from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class PluginSpec:
    name: str
    source: str
    install_mode: str = "copy"


@dataclass(frozen=True)
class InstructionSpec:
    name: str
    source: str
    target: str
    install_mode: str = "copy"


@dataclass(frozen=True)
class HookSpec:
    name: str
    source: str
    target: str = ".codex/hooks.json"


@dataclass(frozen=True)
class Manifest:
    schema_version: int
    name: str
    plugins: list[PluginSpec] = field(default_factory=list)
    instructions: list[InstructionSpec] = field(default_factory=list)
    hooks: list[HookSpec] = field(default_factory=list)
    platform_overrides: dict[str, dict[str, str]] = field(default_factory=dict)

    def plugin_mode_for(self, os_name: str, plugin: PluginSpec) -> str:
        override = self.platform_overrides.get(os_name, {}).get("plugin_install_mode")
        return override or plugin.install_mode

    def instruction_mode_for(self, os_name: str, instruction: InstructionSpec) -> str:
        override = self.platform_overrides.get(os_name, {}).get("instruction_install_mode")
        return override or instruction.install_mode


def load_manifest(path: str | Path) -> Manifest:
    manifest_path = Path(path)
    data = tomllib.loads(manifest_path.read_text(encoding="utf-8"))

    plugins = [
        PluginSpec(
            name=item["name"],
            source=item["source"],
            install_mode=item.get("install_mode", "copy"),
        )
        for item in data.get("plugins", [])
    ]
    instructions = [
        InstructionSpec(
            name=item["name"],
            source=item["source"],
            target=item["target"],
            install_mode=item.get("install_mode", "copy"),
        )
        for item in data.get("instructions", [])
    ]
    hooks = [
        HookSpec(
            name=item["name"],
            source=item["source"],
            target=item.get("target", ".codex/hooks.json"),
        )
        for item in data.get("hooks", [])
    ]

    return Manifest(
        schema_version=int(data["schema_version"]),
        name=data["name"],
        plugins=plugins,
        instructions=instructions,
        hooks=hooks,
        platform_overrides=data.get("platform_overrides", {}),
    )
