"""Command-line interface for the platform builder."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from .blueprint import PlatformBlueprint
from .scaffolder import PlatformScaffolder


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and scaffold platform blueprints.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a blueprint JSON file")
    create_parser.add_argument("--name", required=True, help="Platform name")
    create_parser.add_argument("--description", required=True, help="Platform description")
    create_parser.add_argument("--feature", action="append", default=[], help="Feature to include")
    create_parser.add_argument(
        "--service",
        action="append",
        default=[],
        help="Service definition as name:details (e.g., api:'REST endpoints')",
    )
    create_parser.add_argument("--output", type=Path, default=Path("blueprint.json"), help="Output file")

    scaffold_parser = subparsers.add_parser("scaffold", help="Scaffold a platform from an existing blueprint")
    scaffold_parser.add_argument("blueprint", type=Path, help="Path to blueprint JSON")
    scaffold_parser.add_argument("--output", type=Path, default=Path("platform"), help="Target directory")

    return parser


def parse_services(service_args: List[str]) -> dict[str, str]:
    services: dict[str, str] = {}
    for raw in service_args:
        name, _, details = raw.partition(":")
        name = name.strip()
        details = details.strip(" \"")
        if not name:
            raise ValueError("Service entries must include a name before the colon")
        services[name] = details or ""
    return services


def handle_create(args: argparse.Namespace) -> Path:
    blueprint = PlatformBlueprint(
        name=args.name,
        description=args.description,
        features=args.feature,
        services=parse_services(args.service),
    )
    scaffolder = PlatformScaffolder(blueprint)
    return scaffolder.write_blueprint(args.output)


def handle_scaffold(args: argparse.Namespace) -> list[Path]:
    data = json.loads(args.blueprint.read_text(encoding="utf-8"))
    blueprint = PlatformBlueprint.from_dict(data)
    scaffolder = PlatformScaffolder(blueprint)
    return list(scaffolder.scaffold(args.output))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "create":
        output = handle_create(args)
        print(f"Blueprint written to {output}")
        return 0

    if args.command == "scaffold":
        created = handle_scaffold(args)
        print(f"Created {len(created)} paths under {args.output}")
        return 0

    parser.error("Unknown command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
