"""Rollen-Adapter: fuer Rollen, deren Aufloesung bereits vollstaendig von einem
eigenen Modul geleistet wird, delegiert die Stufenleiter dorthin statt eine zweite,
unabhaengig driftende Aufloesung zu bauen (Faustregel aus Nachtrag 2 des Tickets:
"Was sich beim Kopieren auseinanderentwickeln kann, wird nicht kopiert, sondern
aufgerufen"). Neue Adapter tragen sich hier in ADAPTERS ein."""

from source_resolver.adapters.policy_registry import resolve_policy_registry
from source_resolver.adapters.bach_tool_registry import resolve_bach_tool_registry

ADAPTERS = {
    "policy.registry": resolve_policy_registry,
    "resources.bach.tool_registry": resolve_bach_tool_registry,
}

__all__ = ["ADAPTERS"]
