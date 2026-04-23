from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import shutil
import subprocess
import time

from .manifest import HookSpec, InstructionSpec, Manifest, PluginSpec, load_manifest
from .platforms import ManagedPaths, resolve_target_path


MANIFEST_NAME = "codex-env.toml"
LEGACY_PLUGIN_OVERLAY_NAMES = {
    "jy-env-core": ["codex-env-core"],
}


@dataclass
class ApplyItem:
    name: str
    destination: Path
    action: str
    detail: str


@dataclass
class ApplyReport:
    repo_root: Path
    os_name: str
    plugins: list[ApplyItem] = field(default_factory=list)
    skills: list[ApplyItem] = field(default_factory=list)
    instructions: list[ApplyItem] = field(default_factory=list)
    hooks: list[ApplyItem] = field(default_factory=list)
    marketplace_action: str = "skipped"
    state_path: Path | None = None
    managed_repo: Path | None = None


def slugify_repo_name(git_url: str) -> str:
    normalized = normalize_repo_identifier(git_url)
    slug = normalized.rstrip("/\\").split("/")[-1].split("\\")[-1]
    if slug.endswith(".git"):
        slug = slug[:-4]
    safe = "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in slug)
    suffix = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]
    if safe:
        return f"{safe}-{suffix}"
    return f"codex-env-{suffix}"


def normalize_repo_identifier(git_url: str) -> str:
    normalized = git_url.strip()
    if "://" in normalized or normalized.startswith("git@"):
        return normalized.rstrip("/")
    return str(Path(normalized).expanduser().resolve())


def hash_path(path: Path) -> str:
    digest = hashlib.sha256()

    if path.is_file():
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
        return digest.hexdigest()

    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(str(file_path.relative_to(path)).encode("utf-8"))
        digest.update(file_path.read_bytes())

    return digest.hexdigest()


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"plugins": {}, "skills": {}, "instructions": {}, "hooks": {}, "last_apply": None}

    state = json.loads(path.read_text(encoding="utf-8"))
    state.setdefault("plugins", {})
    state.setdefault("skills", {})
    state.setdefault("instructions", {})
    state.setdefault("hooks", {})
    state.setdefault("last_apply", None)
    return state


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def replace_path(destination: Path) -> None:
    if destination.is_symlink() or destination.is_file():
        destination.unlink()
        return
    if destination.is_dir():
        shutil.rmtree(destination)


def copy_directory(source: Path, destination: Path) -> None:
    replace_path(destination)
    shutil.copytree(source, destination)


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        replace_path(destination)
    shutil.copy2(source, destination)


def symlink_path(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        replace_path(destination)
    destination.symlink_to(source.resolve(), target_is_directory=source.is_dir())


def is_symlink_to(destination: Path, source: Path) -> bool:
    try:
        return destination.is_symlink() and destination.resolve() == source.resolve()
    except FileNotFoundError:
        return False


def _load_json_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def _deep_merge(base: dict, overlay: dict) -> dict:
    merged = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
            continue
        merged[key] = value
    return merged


def merge_plugin_mcp_overlay(plugin_dir: Path, overlay_path: Path) -> None:
    target_path = plugin_dir / ".mcp.json"
    base = {"mcpServers": {}}
    if target_path.exists():
        base = _load_json_object(target_path)

    overlay = _load_json_object(overlay_path)
    merged = _deep_merge(base, overlay)
    target_path.write_text(json.dumps(merged, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def resolve_plugin_overlay_path(plugin_name: str, paths: ManagedPaths) -> tuple[Path | None, str | None]:
    preferred = paths.local_plugin_overlay_root / f"{plugin_name}.mcp.json"
    if preferred.exists():
        return preferred, "local mcp overlay"

    for legacy_name in LEGACY_PLUGIN_OVERLAY_NAMES.get(plugin_name, []):
        candidate = paths.local_plugin_overlay_root / f"{legacy_name}.mcp.json"
        if candidate.exists():
            return candidate, "legacy local mcp overlay fallback"

    return None, None


def _existing_copy_hash(path: Path) -> str | None:
    if not path.exists() or path.is_symlink():
        return None
    return hash_path(path)


def _plugin_state(
    source: Path,
    mode: str,
    desired_hash: str,
    overlay_hash: str | None,
    installed_hash: str | None = None,
) -> dict:
    return {
        "hash": desired_hash,
        "mode": mode,
        "overlay_hash": overlay_hash,
        "installed_hash": installed_hash,
        "source": str(source),
    }


def _instruction_state(
    destination: Path,
    mode: str,
    desired_hash: str,
    installed_hash: str | None = None,
) -> dict:
    return {
        "hash": desired_hash,
        "mode": mode,
        "installed_hash": installed_hash,
        "target": str(destination),
    }


def _hook_state(
    source: Path,
    destination: Path,
    desired_hash: str,
    managed_hooks: dict,
) -> dict:
    return {
        "hash": desired_hash,
        "source": str(source),
        "target": str(destination),
        "managed_hooks": managed_hooks,
    }


def _skill_state(
    destination: Path,
    mode: str,
    desired_hash: str,
    installed_hash: str | None = None,
) -> dict:
    return {
        "hash": desired_hash,
        "mode": mode,
        "installed_hash": installed_hash,
        "target": str(destination),
    }


def _remove_managed_plugin(plugin_name: str, paths: ManagedPaths, state: dict) -> ApplyItem:
    destination = paths.plugin_root / plugin_name
    existed = destination.exists() or destination.is_symlink()
    if existed:
        replace_path(destination)
    state["plugins"].pop(plugin_name, None)
    detail = "removed stale managed plugin" if existed else "cleared stale managed plugin state"
    action = "removed" if existed else "skipped"
    return ApplyItem(plugin_name, destination, action, detail)


def _remove_managed_skill(plugin_name: str, paths: ManagedPaths, state: dict) -> ApplyItem:
    destination = paths.skills_root / plugin_name
    existed = destination.exists() or destination.is_symlink()
    if existed:
        replace_path(destination)
    state["skills"].pop(plugin_name, None)
    detail = "removed stale managed skill link" if existed else "cleared stale managed skill state"
    action = "removed" if existed else "skipped"
    return ApplyItem(plugin_name, destination, action, detail)


def _remove_managed_instruction(name: str, state: dict) -> ApplyItem:
    previous = state["instructions"].get(name, {})
    destination = Path(previous["target"]) if previous.get("target") else Path(name)
    existed = destination.exists() or destination.is_symlink()
    if existed:
        replace_path(destination)
    state["instructions"].pop(name, None)
    detail = "removed stale managed instruction" if existed else "cleared stale managed instruction state"
    action = "removed" if existed else "skipped"
    return ApplyItem(name, destination, action, detail)


def _hook_marker(name: str) -> str:
    return f"[codex-env-sync:{name}]"


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _load_hooks_document(path: Path) -> dict:
    if not path.exists():
        return {"hooks": {}}

    data = _load_json_object(path)
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError(f"Expected hooks object in {path}")
    return data


def _ensure_managed_marker(document: dict, name: str) -> dict:
    marker = _hook_marker(name)
    managed = deepcopy(document)
    for groups in managed.get("hooks", {}).values():
        if not isinstance(groups, list):
            continue
        for group in groups:
            for handler in group.get("hooks", []):
                if handler.get("type") != "command":
                    continue
                command = handler.get("command")
                if not isinstance(command, str) or marker in command:
                    continue
                handler["command"] = f"{command} # {marker}"
    return managed


def _previous_managed_handler_keys(previous_managed_hooks: dict | None) -> set[str]:
    keys: set[str] = set()
    if not isinstance(previous_managed_hooks, dict):
        return keys
    for groups in previous_managed_hooks.get("hooks", {}).values():
        if not isinstance(groups, list):
            continue
        for group in groups:
            for handler in group.get("hooks", []):
                keys.add(_canonical_json(handler))
    return keys


def _handler_is_managed(handler: dict, name: str, previous_keys: set[str]) -> bool:
    command = handler.get("command")
    if isinstance(command, str) and _hook_marker(name) in command:
        return True
    return _canonical_json(handler) in previous_keys


def _strip_managed_hooks(current: dict, name: str, previous_managed_hooks: dict | None) -> dict:
    stripped = deepcopy(current)
    previous_keys = _previous_managed_handler_keys(previous_managed_hooks)
    hooks = stripped.setdefault("hooks", {})

    for event_name in list(hooks):
        groups = hooks[event_name]
        if not isinstance(groups, list):
            continue

        kept_groups = []
        for group in groups:
            handlers = group.get("hooks", [])
            if not isinstance(handlers, list):
                kept_groups.append(group)
                continue

            kept_handlers = [
                handler
                for handler in handlers
                if not (isinstance(handler, dict) and _handler_is_managed(handler, name, previous_keys))
            ]
            if kept_handlers:
                next_group = dict(group)
                next_group["hooks"] = kept_handlers
                kept_groups.append(next_group)

        if kept_groups:
            hooks[event_name] = kept_groups
        else:
            hooks.pop(event_name)

    return stripped


def _merge_managed_hooks(current: dict, managed: dict, name: str, previous_managed_hooks: dict | None) -> dict:
    merged = _strip_managed_hooks(current, name, previous_managed_hooks)
    hooks = merged.setdefault("hooks", {})
    for event_name, groups in managed.get("hooks", {}).items():
        if not isinstance(groups, list) or not groups:
            continue
        hooks.setdefault(event_name, []).extend(deepcopy(groups))
    return merged


def _hooks_text(document: dict) -> str:
    return json.dumps(document, indent=2, sort_keys=False) + "\n"


def _remove_managed_hook(name: str, state: dict) -> ApplyItem:
    previous = state["hooks"].get(name, {})
    destination = Path(previous["target"]) if previous.get("target") else Path(name)
    previous_managed_hooks = previous.get("managed_hooks")

    if not destination.exists():
        state["hooks"].pop(name, None)
        return ApplyItem(name, destination, "skipped", "cleared stale managed hook state")

    current = _load_hooks_document(destination)
    desired = _strip_managed_hooks(current, name, previous_managed_hooks)
    action = "skipped"
    detail = "cleared stale managed hook state"
    if _canonical_json(current) != _canonical_json(desired):
        destination.write_text(_hooks_text(desired), encoding="utf-8")
        action = "removed"
        detail = "removed stale managed hook entries"

    state["hooks"].pop(name, None)
    return ApplyItem(name, destination, action, detail)


def _apply_plugin(
    plugin: PluginSpec,
    repo_root: Path,
    paths: ManagedPaths,
    manifest: Manifest,
    state: dict,
) -> ApplyItem:
    source = repo_root / plugin.source
    destination = paths.plugin_root / plugin.name
    overlay_path, overlay_detail = resolve_plugin_overlay_path(plugin.name, paths)
    desired_hash = hash_path(source)
    overlay_hash = hash_path(overlay_path) if overlay_path is not None else None
    previous = state["plugins"].get(plugin.name, {})
    mode = manifest.plugin_mode_for(paths.os_name, plugin)

    if mode == "copy":
        installed_hash = _existing_copy_hash(destination)
        if (
            destination.exists()
            and not destination.is_symlink()
            and previous.get("mode") == "copy"
            and previous.get("hash") == desired_hash
            and previous.get("overlay_hash") == overlay_hash
            and previous.get("installed_hash") == installed_hash
        ):
            state["plugins"][plugin.name] = _plugin_state(source, "copy", desired_hash, overlay_hash, installed_hash)
            return ApplyItem(plugin.name, destination, "skipped", "content unchanged")

        copy_directory(source, destination)
        detail = "copied plugin bundle"
        if overlay_path is not None:
            merge_plugin_mcp_overlay(destination, overlay_path)
            detail = f"copied plugin bundle + merged {overlay_detail}"

        installed_hash = hash_path(destination)
        state["plugins"][plugin.name] = _plugin_state(source, "copy", desired_hash, overlay_hash, installed_hash)
        return ApplyItem(plugin.name, destination, "applied", detail)

    if mode == "symlink":
        if overlay_path is not None:
            installed_hash = _existing_copy_hash(destination)
            if (
                destination.exists()
                and not destination.is_symlink()
                and previous.get("mode") == "copy"
                and previous.get("hash") == desired_hash
                and previous.get("overlay_hash") == overlay_hash
                and previous.get("installed_hash") == installed_hash
            ):
                state["plugins"][plugin.name] = _plugin_state(source, "copy", desired_hash, overlay_hash, installed_hash)
                return ApplyItem(
                    plugin.name,
                    destination,
                    "skipped",
                    f"content unchanged (symlink fallback due to {overlay_detail})",
                )

            copy_directory(source, destination)
            merge_plugin_mcp_overlay(destination, overlay_path)
            installed_hash = hash_path(destination)
            state["plugins"][plugin.name] = _plugin_state(source, "copy", desired_hash, overlay_hash, installed_hash)
            return ApplyItem(
                plugin.name,
                destination,
                "applied",
                f"copied plugin bundle + merged {overlay_detail} (symlink fallback due to local overlay)",
            )

        if is_symlink_to(destination, source):
            state["plugins"][plugin.name] = _plugin_state(source, "symlink", desired_hash, overlay_hash)
            return ApplyItem(plugin.name, destination, "skipped", "symlink unchanged")

        symlink_path(source, destination)
        state["plugins"][plugin.name] = _plugin_state(source, "symlink", desired_hash, overlay_hash)
        return ApplyItem(plugin.name, destination, "applied", "symlinked plugin bundle")

    raise ValueError(f"Unsupported plugin install mode for v1: {mode}")


def _plugin_skills_source(destination: Path) -> Path | None:
    manifest_path = destination / ".codex-plugin" / "plugin.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    relative = data.get("skills")
    if not isinstance(relative, str) or not relative:
        return None

    skills_path = destination / Path(relative)
    if not skills_path.exists():
        return None
    return skills_path


def _apply_plugin_skills(
    plugin: PluginSpec,
    paths: ManagedPaths,
    state: dict,
) -> ApplyItem | None:
    plugin_root = paths.plugin_root / plugin.name
    source = _plugin_skills_source(plugin_root)
    if source is None:
        state["skills"].pop(plugin.name, None)
        return None

    destination = paths.skills_root / plugin.name
    desired_hash = hash_path(source)
    previous = state["skills"].get(plugin.name, {})

    if paths.os_name == "windows":
        installed_hash = _existing_copy_hash(destination)
        if (
            destination.exists()
            and not destination.is_symlink()
            and previous.get("mode") == "copy"
            and previous.get("hash") == desired_hash
            and previous.get("installed_hash") == installed_hash
        ):
            state["skills"][plugin.name] = _skill_state(destination, "copy", desired_hash, installed_hash)
            return ApplyItem(plugin.name, destination, "skipped", "skill content unchanged")

        copy_directory(source, destination)
        installed_hash = hash_path(destination)
        state["skills"][plugin.name] = _skill_state(destination, "copy", desired_hash, installed_hash)
        return ApplyItem(plugin.name, destination, "applied", "copied skill directory")

    if is_symlink_to(destination, source):
        state["skills"][plugin.name] = _skill_state(destination, "symlink", desired_hash)
        return ApplyItem(plugin.name, destination, "skipped", "skill symlink unchanged")

    symlink_path(source, destination)
    state["skills"][plugin.name] = _skill_state(destination, "symlink", desired_hash)
    return ApplyItem(plugin.name, destination, "applied", "symlinked skill directory")


def _apply_instruction(
    instruction: InstructionSpec,
    repo_root: Path,
    paths: ManagedPaths,
    manifest: Manifest,
    state: dict,
) -> ApplyItem:
    source = repo_root / instruction.source
    destination = resolve_target_path(paths.home, instruction.target)
    desired_hash = hash_path(source)
    previous = state["instructions"].get(instruction.name, {})
    mode = manifest.instruction_mode_for(paths.os_name, instruction)

    if mode == "copy":
        installed_hash = _existing_copy_hash(destination)
        if (
            destination.exists()
            and not destination.is_symlink()
            and previous.get("mode") == "copy"
            and previous.get("hash") == desired_hash
            and previous.get("installed_hash") == installed_hash
        ):
            state["instructions"][instruction.name] = _instruction_state(destination, "copy", desired_hash, installed_hash)
            return ApplyItem(instruction.name, destination, "skipped", "content unchanged")

        copy_file(source, destination)
        installed_hash = hash_path(destination)
        state["instructions"][instruction.name] = _instruction_state(destination, "copy", desired_hash, installed_hash)
        return ApplyItem(instruction.name, destination, "applied", "copied instruction artifact")

    if mode == "symlink":
        if is_symlink_to(destination, source):
            state["instructions"][instruction.name] = _instruction_state(destination, "symlink", desired_hash)
            return ApplyItem(instruction.name, destination, "skipped", "symlink unchanged")

        symlink_path(source, destination)
        state["instructions"][instruction.name] = _instruction_state(destination, "symlink", desired_hash)
        return ApplyItem(instruction.name, destination, "applied", "symlinked instruction artifact")

    raise ValueError(f"Unsupported instruction install mode for v1: {mode}")


def _apply_hook(
    hook: HookSpec,
    repo_root: Path,
    paths: ManagedPaths,
    state: dict,
) -> ApplyItem:
    source = repo_root / hook.source
    destination = resolve_target_path(paths.home, hook.target)
    if paths.os_name == "windows":
        state["hooks"].pop(hook.name, None)
        return ApplyItem(hook.name, destination, "skipped", "hooks are disabled on windows")

    desired_hash = hash_path(source)
    previous = state["hooks"].get(hook.name, {})
    source_document = _load_hooks_document(source)
    managed_hooks = _ensure_managed_marker(source_document, hook.name)
    current_document = _load_hooks_document(destination)
    desired_document = _merge_managed_hooks(
        current_document,
        managed_hooks,
        hook.name,
        previous.get("managed_hooks"),
    )

    current_text = destination.read_text(encoding="utf-8") if destination.exists() else ""
    desired_text = _hooks_text(desired_document)
    if (
        current_text == desired_text
        and previous.get("hash") == desired_hash
        and previous.get("target") == str(destination)
    ):
        state["hooks"][hook.name] = _hook_state(source, destination, desired_hash, managed_hooks)
        return ApplyItem(hook.name, destination, "skipped", "managed hook entries unchanged")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(desired_text, encoding="utf-8")
    state["hooks"][hook.name] = _hook_state(source, destination, desired_hash, managed_hooks)
    return ApplyItem(hook.name, destination, "applied", "merged managed hook entries")


def _managed_marketplace_entry(plugin_name: str, category: str) -> dict:
    return {
        "name": plugin_name,
        "source": {
            "source": "local",
            "path": f"./plugins/{plugin_name}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": category,
    }


def _plugin_category(repo_root: Path, plugin: PluginSpec) -> str:
    manifest_path = repo_root / plugin.source / ".codex-plugin" / "plugin.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    return data.get("interface", {}).get("category", "Productivity")


def write_marketplace(
    repo_root: Path,
    manifest: Manifest,
    paths: ManagedPaths,
    stale_managed_names: set[str] | None = None,
) -> str:
    existing = {
        "name": "personal-codex",
        "interface": {"displayName": "Personal Codex"},
        "plugins": [],
    }
    if paths.marketplace_path.exists():
        existing = json.loads(paths.marketplace_path.read_text(encoding="utf-8"))
        existing.setdefault("name", "personal-codex")
        existing.setdefault("interface", {"displayName": "Personal Codex"})
        existing.setdefault("plugins", [])

    managed_names = {plugin.name for plugin in manifest.plugins}
    blocked_names = managed_names | (stale_managed_names or set())
    preserved = [entry for entry in existing["plugins"] if entry.get("name") not in blocked_names]
    managed = [
        _managed_marketplace_entry(plugin.name, _plugin_category(repo_root, plugin))
        for plugin in manifest.plugins
    ]

    desired = {
        "name": existing["name"],
        "interface": existing["interface"],
        "plugins": preserved + managed,
    }

    desired_text = json.dumps(desired, indent=2, sort_keys=False) + "\n"
    current_text = paths.marketplace_path.read_text(encoding="utf-8") if paths.marketplace_path.exists() else ""
    if current_text == desired_text:
        return "skipped"

    paths.marketplace_path.parent.mkdir(parents=True, exist_ok=True)
    paths.marketplace_path.write_text(desired_text, encoding="utf-8")
    return "applied"


def apply_environment(repo_root: str | Path, home: str | Path | None = None, os_name: str | None = None) -> ApplyReport:
    repo_path = Path(repo_root).resolve()
    manifest = load_manifest(repo_path / MANIFEST_NAME)
    paths = ManagedPaths.for_platform(os_name=os_name, home=home)
    paths.ensure_parent_dirs()

    state = load_state(paths.state_path)
    report = ApplyReport(repo_root=repo_path, os_name=paths.os_name, state_path=paths.state_path)
    current_plugin_names = {plugin.name for plugin in manifest.plugins}
    previous_plugin_names = set(state["plugins"])
    stale_plugin_names = previous_plugin_names - current_plugin_names
    for plugin_name in sorted(stale_plugin_names):
        report.skills.append(_remove_managed_skill(plugin_name, paths, state))
        report.plugins.append(_remove_managed_plugin(plugin_name, paths, state))

    current_instruction_names = {instruction.name for instruction in manifest.instructions}
    stale_instruction_names = set(state["instructions"]) - current_instruction_names
    for instruction_name in sorted(stale_instruction_names):
        report.instructions.append(_remove_managed_instruction(instruction_name, state))

    current_hook_names = {hook.name for hook in manifest.hooks}
    stale_hook_names = set(state["hooks"]) - current_hook_names
    for hook_name in sorted(stale_hook_names):
        report.hooks.append(_remove_managed_hook(hook_name, state))

    for plugin in manifest.plugins:
        report.plugins.append(_apply_plugin(plugin, repo_path, paths, manifest, state))
        skill_item = _apply_plugin_skills(plugin, paths, state)
        if skill_item is not None:
            report.skills.append(skill_item)

    report.marketplace_action = write_marketplace(repo_path, manifest, paths, stale_managed_names=stale_plugin_names)

    for instruction in manifest.instructions:
        report.instructions.append(_apply_instruction(instruction, repo_path, paths, manifest, state))

    for hook in manifest.hooks:
        report.hooks.append(_apply_hook(hook, repo_path, paths, state))

    state["last_apply"] = int(time.time())
    save_state(paths.state_path, state)
    return report


def clone_or_update_repo(git_url: str, paths: ManagedPaths) -> Path:
    repo_path = paths.repo_cache_root / slugify_repo_name(git_url)
    paths.repo_cache_root.mkdir(parents=True, exist_ok=True)

    if (repo_path / ".git").exists():
        subprocess.run(["git", "-C", str(repo_path), "pull", "--ff-only"], check=True)
        return repo_path

    if repo_path.exists():
        replace_path(repo_path)

    subprocess.run(["git", "clone", git_url, str(repo_path)], check=True)
    return repo_path


def bootstrap_environment(git_url: str, home: str | Path | None = None, os_name: str | None = None) -> ApplyReport:
    paths = ManagedPaths.for_platform(os_name=os_name, home=home)
    paths.ensure_parent_dirs()
    repo_path = clone_or_update_repo(git_url, paths)
    report = apply_environment(repo_path, home=paths.home, os_name=paths.os_name)
    report.managed_repo = repo_path
    return report
