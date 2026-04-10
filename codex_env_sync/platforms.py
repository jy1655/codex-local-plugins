from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import platform


def detect_os_name() -> str:
    system = platform.system().lower()
    if system.startswith("darwin"):
        return "darwin"
    if system.startswith("windows"):
        return "windows"
    return "linux"


@dataclass(frozen=True)
class ManagedPaths:
    os_name: str
    home: Path
    codex_home: Path
    plugin_root: Path
    marketplace_path: Path
    repo_cache_root: Path
    state_path: Path
    local_plugin_overlay_root: Path

    @classmethod
    def for_platform(cls, os_name: str | None = None, home: str | Path | None = None) -> "ManagedPaths":
        resolved_os = (os_name or detect_os_name()).lower()
        resolved_home = Path(home).expanduser() if home is not None else Path.home()
        return cls(
            os_name=resolved_os,
            home=resolved_home,
            codex_home=resolved_home / ".codex",
            plugin_root=resolved_home / "plugins",
            marketplace_path=resolved_home / ".agents" / "plugins" / "marketplace.json",
            repo_cache_root=resolved_home / ".codex-env-sync" / "repos",
            state_path=resolved_home / ".codex-env-sync" / "state.json",
            local_plugin_overlay_root=resolved_home / ".codex-env-sync" / "local" / "plugins",
        )

    def ensure_parent_dirs(self) -> None:
        self.codex_home.mkdir(parents=True, exist_ok=True)
        self.plugin_root.mkdir(parents=True, exist_ok=True)
        self.marketplace_path.parent.mkdir(parents=True, exist_ok=True)
        self.repo_cache_root.mkdir(parents=True, exist_ok=True)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.local_plugin_overlay_root.mkdir(parents=True, exist_ok=True)


def resolve_target_path(home: Path, target: str) -> Path:
    if target.startswith("~/") or target.startswith("~\\"):
        return Path(target).expanduser()

    candidate = Path(target)
    if candidate.is_absolute():
        return candidate

    return home / candidate
