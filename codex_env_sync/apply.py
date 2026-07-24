from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import os
import shutil
import subprocess
import time
import uuid

from .manifest import InstructionSpec, Manifest, PluginSpec, load_manifest
from .platforms import ManagedPaths, resolve_target_path


MANIFEST_NAME = "codex-env.toml"


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
    plugin_installs: list[ApplyItem] = field(default_factory=list)
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
    write_text_atomic(path, json.dumps(state, indent=2, sort_keys=True) + "\n")


def replace_path(destination: Path) -> None:
    if destination.is_symlink() or destination.is_file():
        destination.unlink()
        return
    if destination.is_dir():
        shutil.rmtree(destination)


def copy_directory(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.parent / f".{destination.name}.tmp-{uuid.uuid4().hex}"
    backup = destination.parent / f".{destination.name}.old-{uuid.uuid4().hex}"
    shutil.copytree(source, staging)
    had_destination = destination.exists() or destination.is_symlink()
    try:
        if had_destination:
            destination.rename(backup)
        staging.rename(destination)
    except Exception:
        if not destination.exists() and backup.exists():
            backup.rename(destination)
        raise
    finally:
        if staging.exists():
            replace_path(staging)
    if backup.exists() or backup.is_symlink():
        replace_path(backup)


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.parent / f".{destination.name}.tmp-{uuid.uuid4().hex}"
    shutil.copy2(source, staging)
    if destination.is_dir() and not destination.is_symlink():
        replace_path(destination)
    staging.replace(destination)


def write_text_atomic(destination: Path, text: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.parent / f".{destination.name}.tmp-{uuid.uuid4().hex}"
    try:
        staging.write_text(text, encoding="utf-8")
        staging.replace(destination)
    finally:
        if staging.exists():
            staging.unlink()


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


def _existing_copy_hash(path: Path) -> str | None:
    if not path.exists() or path.is_symlink():
        return None
    return hash_path(path)


def _plugin_state(
    source: Path,
    mode: str,
    desired_hash: str,
    installed_hash: str | None = None,
) -> dict:
    return {
        "hash": desired_hash,
        "mode": mode,
        "installed_hash": installed_hash,
        "source": str(source),
    }


def _instruction_state(
    source: Path,
    destination: Path,
    mode: str,
    desired_hash: str,
    installed_hash: str | None = None,
) -> dict:
    return {
        "hash": desired_hash,
        "mode": mode,
        "installed_hash": installed_hash,
        "source": str(source),
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
        write_text_atomic(destination, _hooks_text(desired))
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
    mode_override: str | None = None,
) -> ApplyItem:
    source = repo_root / plugin.source
    destination = paths.plugin_root / plugin.name
    desired_hash = hash_path(source)
    previous = state["plugins"].get(plugin.name, {})
    mode = mode_override or manifest.plugin_mode_for(paths.os_name, plugin)

    if mode == "copy":
        installed_hash = _existing_copy_hash(destination)
        if (
            destination.exists()
            and not destination.is_symlink()
            and previous.get("mode") == "copy"
            and previous.get("hash") == desired_hash
            and previous.get("installed_hash") == installed_hash
        ):
            state["plugins"][plugin.name] = _plugin_state(source, "copy", desired_hash, installed_hash)
            return ApplyItem(plugin.name, destination, "skipped", "content unchanged")

        copy_directory(source, destination)
        installed_hash = hash_path(destination)
        state["plugins"][plugin.name] = _plugin_state(source, "copy", desired_hash, installed_hash)
        return ApplyItem(plugin.name, destination, "applied", "copied plugin bundle")

    if mode == "symlink":
        if is_symlink_to(destination, source):
            state["plugins"][plugin.name] = _plugin_state(source, "symlink", desired_hash)
            return ApplyItem(plugin.name, destination, "skipped", "symlink unchanged")

        symlink_path(source, destination)
        state["plugins"][plugin.name] = _plugin_state(source, "symlink", desired_hash)
        return ApplyItem(plugin.name, destination, "applied", "symlinked plugin bundle")

    raise ValueError(f"Unsupported plugin install mode for v1: {mode}")


def _apply_instruction(
    instruction: InstructionSpec,
    repo_root: Path,
    paths: ManagedPaths,
    manifest: Manifest,
    state: dict,
    mode_override: str | None = None,
) -> ApplyItem:
    source = repo_root / instruction.source
    destination = resolve_target_path(paths.home, instruction.target)
    desired_hash = hash_path(source)
    previous = state["instructions"].get(instruction.name, {})
    mode = mode_override or manifest.instruction_mode_for(paths.os_name, instruction)

    if mode == "copy":
        installed_hash = _existing_copy_hash(destination)
        if (
            destination.exists()
            and not destination.is_symlink()
            and previous.get("mode") == "copy"
            and previous.get("hash") == desired_hash
            and previous.get("installed_hash") == installed_hash
        ):
            state["instructions"][instruction.name] = _instruction_state(
                source, destination, "copy", desired_hash, installed_hash
            )
            return ApplyItem(instruction.name, destination, "skipped", "content unchanged")

        copy_file(source, destination)
        installed_hash = hash_path(destination)
        state["instructions"][instruction.name] = _instruction_state(
            source, destination, "copy", desired_hash, installed_hash
        )
        return ApplyItem(instruction.name, destination, "applied", "copied instruction artifact")

    if mode == "symlink":
        if is_symlink_to(destination, source):
            state["instructions"][instruction.name] = _instruction_state(
                source, destination, "symlink", desired_hash
            )
            return ApplyItem(instruction.name, destination, "skipped", "symlink unchanged")

        symlink_path(source, destination)
        state["instructions"][instruction.name] = _instruction_state(
            source, destination, "symlink", desired_hash
        )
        return ApplyItem(instruction.name, destination, "applied", "symlinked instruction artifact")

    raise ValueError(f"Unsupported instruction install mode for v1: {mode}")


def _managed_marketplace_entry(plugin: PluginSpec, category: str) -> dict:
    return {
        "name": plugin.name,
        "source": {
            "source": "local",
            "path": f"./plugins/{plugin.name}",
        },
        "policy": {
            "installation": plugin.installation_policy,
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
        _managed_marketplace_entry(plugin, _plugin_category(repo_root, plugin))
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

    write_text_atomic(paths.marketplace_path, desired_text)
    return "applied"


def _install_default_plugins(manifest: Manifest, paths: ManagedPaths) -> list[ApplyItem]:
    default_plugins = [
        plugin
        for plugin in manifest.plugins
        if plugin.installation_policy == "INSTALLED_BY_DEFAULT"
    ]
    if not default_plugins:
        return []

    marketplace = _load_json_object(paths.marketplace_path)
    marketplace_name = marketplace.get("name")
    if not isinstance(marketplace_name, str) or not marketplace_name:
        raise ValueError(f"Marketplace name is missing from {paths.marketplace_path}")

    codex_executable = shutil.which("codex")
    if codex_executable is None:
        raise RuntimeError(
            "Codex CLI is required to install plugins marked INSTALLED_BY_DEFAULT"
        )

    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(paths.codex_home)
    if paths.os_name == "windows":
        environment["USERPROFILE"] = str(paths.home)
    else:
        environment["HOME"] = str(paths.home)

    installed: list[ApplyItem] = []
    for plugin in default_plugins:
        selector = f"{plugin.name}@{marketplace_name}"
        try:
            completed = subprocess.run(
                [codex_executable, "plugin", "add", selector],
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )
        except OSError as exc:
            raise RuntimeError(f"Failed to start Codex CLI at {codex_executable}") from exc

        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "unknown error").strip()
            raise RuntimeError(f"Failed to install default plugin {selector}: {detail}")

        installed.append(
            ApplyItem(
                plugin.name,
                paths.codex_home,
                "applied",
                f"installed and enabled via codex plugin add ({selector})",
            )
        )
    return installed


def _require_unique_names(items: list, label: str) -> None:
    names = [item.name for item in items]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"Duplicate {label} names: {', '.join(duplicates)}")


def _repo_source(repo_root: Path, relative: str, label: str) -> Path:
    source = (repo_root / relative).resolve()
    if not source.is_relative_to(repo_root):
        raise ValueError(f"{label} source escapes repo root: {relative}")
    return source


def _managed_path_matches_state(destination: Path, previous: dict) -> bool:
    if not destination.exists() and not destination.is_symlink():
        return True

    mode = previous.get("mode")
    if mode == "copy":
        expected_hash = previous.get("installed_hash")
        return isinstance(expected_hash, str) and _existing_copy_hash(destination) == expected_hash
    if mode == "symlink":
        expected_source = previous.get("source")
        return isinstance(expected_source, str) and is_symlink_to(destination, Path(expected_source))
    return False


def _validate_stale_managed_paths(manifest: Manifest, paths: ManagedPaths, state: dict) -> None:
    current_plugin_names = {plugin.name for plugin in manifest.plugins}
    stale_plugin_names = set(state["plugins"]) - current_plugin_names
    for plugin_name in sorted(stale_plugin_names):
        destination = paths.plugin_root / plugin_name
        if not _managed_path_matches_state(destination, state["plugins"].get(plugin_name, {})):
            raise ValueError(f"Refusing to remove modified managed plugin: {destination}")

    for plugin_name in sorted(state["skills"]):
        skill_destination = paths.skills_root / plugin_name
        if not _managed_path_matches_state(skill_destination, state["skills"].get(plugin_name, {})):
            raise ValueError(f"Refusing to remove modified managed skill surface: {skill_destination}")

    current_instruction_names = {instruction.name for instruction in manifest.instructions}
    stale_instruction_names = set(state["instructions"]) - current_instruction_names
    for instruction_name in sorted(stale_instruction_names):
        previous = state["instructions"].get(instruction_name, {})
        destination = Path(previous["target"]) if previous.get("target") else Path(instruction_name)
        if not _managed_path_matches_state(destination, previous):
            raise ValueError(f"Refusing to remove modified managed instruction: {destination}")


def validate_environment(
    repo_root: Path,
    manifest: Manifest,
    paths: ManagedPaths,
    state: dict,
    snapshot: bool = False,
) -> None:
    _require_unique_names(manifest.plugins, "plugin")
    _require_unique_names(manifest.instructions, "instruction")

    for plugin in manifest.plugins:
        source = _repo_source(repo_root, plugin.source, "Plugin")
        if not source.is_dir():
            raise ValueError(f"Plugin source does not exist or is not a directory: {source}")
        mode = "copy" if snapshot else manifest.plugin_mode_for(paths.os_name, plugin)
        if mode not in {"copy", "symlink"}:
            raise ValueError(f"Unsupported plugin install mode for v1: {mode}")
        if plugin.installation_policy not in {
            "AVAILABLE",
            "INSTALLED_BY_DEFAULT",
            "NOT_AVAILABLE",
        }:
            raise ValueError(
                f"Unsupported plugin installation policy: {plugin.installation_policy}"
            )

        plugin_manifest_path = source / ".codex-plugin" / "plugin.json"
        if not plugin_manifest_path.is_file():
            raise ValueError(f"Plugin manifest does not exist: {plugin_manifest_path}")
        plugin_manifest = _load_json_object(plugin_manifest_path)
        skills_relative = plugin_manifest.get("skills")
        if isinstance(skills_relative, str) and skills_relative:
            skills_source = (source / skills_relative).resolve()
            if not skills_source.is_relative_to(source) or not skills_source.is_dir():
                raise ValueError(f"Plugin skills source does not exist or escapes plugin root: {skills_source}")

    for instruction in manifest.instructions:
        source = _repo_source(repo_root, instruction.source, "Instruction")
        if not source.is_file():
            raise ValueError(f"Instruction source does not exist or is not a file: {source}")
        mode = "copy" if snapshot else manifest.instruction_mode_for(paths.os_name, instruction)
        if mode not in {"copy", "symlink"}:
            raise ValueError(f"Unsupported instruction install mode for v1: {mode}")

    if paths.marketplace_path.exists():
        marketplace = _load_json_object(paths.marketplace_path)
        plugins = marketplace.get("plugins", [])
        if not isinstance(plugins, list):
            raise ValueError(f"Expected plugins list in {paths.marketplace_path}")

    _validate_stale_managed_paths(manifest, paths, state)


def apply_environment(
    repo_root: str | Path,
    home: str | Path | None = None,
    os_name: str | None = None,
    snapshot: bool = False,
    install_defaults: bool = False,
) -> ApplyReport:
    repo_path = Path(repo_root).resolve()
    manifest = load_manifest(repo_path / MANIFEST_NAME)
    paths = ManagedPaths.for_platform(os_name=os_name, home=home)
    state = load_state(paths.state_path)
    validate_environment(repo_path, manifest, paths, state, snapshot=snapshot)
    paths.ensure_parent_dirs()

    report = ApplyReport(repo_root=repo_path, os_name=paths.os_name, state_path=paths.state_path)
    current_plugin_names = {plugin.name for plugin in manifest.plugins}
    previous_plugin_names = set(state["plugins"])
    stale_plugin_names = previous_plugin_names - current_plugin_names
    for plugin_name in sorted(stale_plugin_names):
        report.skills.append(_remove_managed_skill(plugin_name, paths, state))
        report.plugins.append(_remove_managed_plugin(plugin_name, paths, state))

    for plugin_name in sorted(state["skills"]):
        report.skills.append(_remove_managed_skill(plugin_name, paths, state))

    current_instruction_names = {instruction.name for instruction in manifest.instructions}
    stale_instruction_names = set(state["instructions"]) - current_instruction_names
    for instruction_name in sorted(stale_instruction_names):
        report.instructions.append(_remove_managed_instruction(instruction_name, state))

    for hook_name in sorted(state["hooks"]):
        report.hooks.append(_remove_managed_hook(hook_name, state))

    for plugin in manifest.plugins:
        mode_override = "copy" if snapshot else None
        report.plugins.append(_apply_plugin(plugin, repo_path, paths, manifest, state, mode_override=mode_override))

    report.marketplace_action = write_marketplace(repo_path, manifest, paths, stale_managed_names=stale_plugin_names)

    for instruction in manifest.instructions:
        mode_override = "copy" if snapshot else None
        report.instructions.append(
            _apply_instruction(instruction, repo_path, paths, manifest, state, mode_override=mode_override)
        )

    state["last_apply"] = int(time.time())
    save_state(paths.state_path, state)
    if install_defaults:
        report.plugin_installs.extend(_install_default_plugins(manifest, paths))
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


def bootstrap_environment(
    git_url: str,
    home: str | Path | None = None,
    os_name: str | None = None,
    install_defaults: bool = True,
) -> ApplyReport:
    paths = ManagedPaths.for_platform(os_name=os_name, home=home)
    paths.ensure_parent_dirs()
    repo_path = clone_or_update_repo(git_url, paths)
    report = apply_environment(
        repo_path,
        home=paths.home,
        os_name=paths.os_name,
        snapshot=True,
        install_defaults=install_defaults,
    )
    report.managed_repo = repo_path
    return report
