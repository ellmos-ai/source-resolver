"""CLI: `source-resolver resolve|confirm|list-roles|check-pointer`."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from source_resolver.ladder import confirm, resolve
from source_resolver.pointer_check import check_pointer
from source_resolver.store import UserSourceStore


def _print(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="source-resolver",
        description="Rollenbasierte Quellenaufloesung fuer Skills (Stufenleiter 0-4).",
    )
    parser.add_argument("--store", help="Pfad zum Stufe-0-Speicher (Default: ~/.source-resolver/config.json)")
    commands = parser.add_subparsers(dest="command", required=True)

    r = commands.add_parser("resolve", help="Rolle aufloesen")
    r.add_argument("rolle")
    r.add_argument("--scope", help="Fuer Rollen mit Adapter (z.B. policy.registry) erforderlich")
    r.add_argument("--query", default="")
    r.add_argument("--discovery-root", action="append", default=[], help="Wiederholbar")
    r.add_argument("--home", help="Ueberschreibt Path.home() (fuer Tests/andere Hosts)")

    c = commands.add_parser("confirm", help="Stufe-2/3-Ergebnis oder manuelle Angabe auf Stufe 0 heben")
    c.add_argument("rolle")
    c.add_argument("quelle_json", help="JSON-String oder Pfad zu einer JSON-Datei")
    c.add_argument("--stufe-herkunft", type=int, default=2)
    c.add_argument("--bestaetigt-von", default="user")

    commands.add_parser("list-roles", help="Alle Stufe-0-Eintraege auflisten")

    cp = commands.add_parser("check-pointer", help="pointer.module_path auf Existenz pruefen")
    cp.add_argument("raw_path")

    args = parser.parse_args(argv)
    store = UserSourceStore(Path(args.store)) if args.store else UserSourceStore()

    if args.command == "resolve":
        roots = [Path(p) for p in args.discovery_root]
        home = Path(args.home) if args.home else None
        result = resolve(
            args.rolle, scope=args.scope, query=args.query, discovery_roots=roots, store=store, home=home
        )
        _print(result.to_dict())
        return 0 if result.status == "resolved" else 2

    if args.command == "confirm":
        raw = args.quelle_json
        quelle_path = Path(raw)
        quelle = json.loads(quelle_path.read_text(encoding="utf-8")) if quelle_path.exists() else json.loads(raw)
        entry = confirm(
            args.rolle, quelle, stufe_herkunft=args.stufe_herkunft, bestaetigt_von=args.bestaetigt_von, store=store
        )
        _print(entry.to_dict())
        return 0

    if args.command == "list-roles":
        roles = store.list_roles()
        _print({name: entry.to_dict() for name, entry in roles.items()})
        return 0

    if args.command == "check-pointer":
        result = check_pointer(args.raw_path)
        _print(result.__dict__)
        return 0 if result.exists else 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
