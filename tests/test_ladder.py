import json
from pathlib import Path

import source_resolver.adapters.policy_registry as pr_adapter
import source_resolver.ladder as ladder
from source_resolver.ladder import ResolutionStatus, Stufe, confirm, resolve
from source_resolver.store import RoleEntry, UserSourceStore, now_iso


def make_fake_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    decisions = home / "OneDrive" / ".TOPICS" / "_control-center" / "_DECISIONS"
    decisions.mkdir(parents=True)
    (decisions / "TO-DECIDE-USER.txt").write_text("offene Entscheidungen", encoding="utf-8")
    return home


def test_stufe1_resolves_known_module_automatically(tmp_path):
    home = make_fake_home(tmp_path)
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("decisions.ledger", store=store, home=home)
    assert result.stufe == Stufe.EIGENES_MODUL
    assert result.status == ResolutionStatus.RESOLVED
    assert "_DECISIONS" in result.quelle["module_path"]


def test_stufe1_resources_inventory_resolves_via_module_path(tmp_path):
    """CR11=C Hoheits-Fassung (T-20260824-339847482): resources.inventory
    zeigt auf .SYNC/_inventory/inventory.db -- module_path+target wie
    decisions.ledger, kein CLI/Adapter (inventory.db hat keine Query-CLI)."""
    home = tmp_path / "home"
    inventory_dir = home / "OneDrive" / ".SYNC" / "_inventory"
    inventory_dir.mkdir(parents=True)
    (inventory_dir / "inventory.db").write_bytes(b"")
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("resources.inventory", store=store, home=home)
    assert result.stufe == Stufe.EIGENES_MODUL
    assert result.status == ResolutionStatus.RESOLVED
    assert result.quelle["id"] == "sync-inventory"
    assert "_inventory" in result.quelle["module_path"]


def test_stufe1_memory_organic_resolves_via_cli_presence(tmp_path, monkeypatch):
    """K3=C (T-20260825-342866657): memory.organic (Gardener) wird ueber einen
    einfachen CLI-Praesenzcheck aufgeloest, nicht ueber einen Modulordner-Pfad --
    Gardener ist pip/editable-installiert, kein fester Ordner unter <HOME>."""
    monkeypatch.setattr(ladder.shutil, "which", lambda name: "/usr/bin/gardener" if name == "gardener" else None)
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("memory.organic", store=store, home=tmp_path / "home")
    assert result.stufe == Stufe.EIGENES_MODUL
    assert result.status == ResolutionStatus.RESOLVED
    assert result.quelle["cli"] == "gardener"
    assert result.quelle["resolved_path"] == "/usr/bin/gardener"


def test_stufe1_memory_curated_resolves_via_cli_presence(tmp_path, monkeypatch):
    """Gegenstueck fuer memory.curated (USMC), gleiches Verfahren."""
    monkeypatch.setattr(ladder.shutil, "which", lambda name: "/usr/bin/usmc" if name == "usmc" else None)
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("memory.curated", store=store, home=tmp_path / "home")
    assert result.stufe == Stufe.EIGENES_MODUL
    assert result.status == ResolutionStatus.RESOLVED
    assert result.quelle["cli"] == "usmc"


def test_stufe1_memory_roles_fall_through_when_cli_absent(tmp_path, monkeypatch):
    """Fehlt gardener/usmc auf PATH, ist das echte Abwesenheit -- Stufe 1 liefert kein
    Ergebnis, die Leiter faellt weiter durch (hier bis Stufe 4, da keine Discovery-
    Wurzeln uebergeben wurden)."""
    monkeypatch.setattr(ladder.shutil, "which", lambda name: None)
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("memory.organic", store=store, home=tmp_path / "home")
    assert result.stufe == Stufe.NICHT_GEFUNDEN
    assert result.status == ResolutionStatus.NOT_FOUND


def test_stufe0_user_override_wins_over_present_module(tmp_path):
    """Kernanforderung aus Nachtrag 1: der Nutzer ueberschreibt auch ein vorhandenes,
    funktionierendes eigenes Modul."""
    home = make_fake_home(tmp_path)
    store = UserSourceStore(tmp_path / "store.json")
    store.set(RoleEntry(
        rolle="decisions.ledger", aktiv=True,
        quelle={"pfad": "/mein/eigener/ort/DECISIONS.md"},
        stufe=0, bestaetigt_am=now_iso(), bestaetigt_von="user", herkunft="manuell",
    ))
    result = resolve("decisions.ledger", store=store, home=home)
    assert result.stufe == Stufe.NUTZER_KONFIGURATION
    assert result.quelle["pfad"] == "/mein/eigener/ort/DECISIONS.md"


def test_stufe1_reports_pointer_drift_when_target_missing(tmp_path):
    """Regressionsklasse T-20260815-603417673: Modulordner da, Zieldatei weg."""
    home = tmp_path / "home"
    (home / "OneDrive" / ".TOPICS" / "_control-center" / "_TOM-lm" / "avatar").mkdir(parents=True)
    # START.md absichtlich NICHT anlegen -> Ziel fehlt
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("user.model", store=store, home=home)
    assert result.status == ResolutionStatus.MODULE_PRESENT_NOT_CALLABLE
    assert "Pointer-Drift" in result.nachricht or "fehlt" in result.nachricht


def test_stufe4_dialog_when_nothing_found(tmp_path):
    home = tmp_path / "home"  # komplett leer, kein Modul vorhanden
    home.mkdir()
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("decisions.ledger", store=store, home=home)
    assert result.stufe == Stufe.NICHT_GEFUNDEN
    assert result.status == ResolutionStatus.NOT_FOUND
    assert result.dialog is not None
    assert "frage_1" in result.dialog
    assert "frage_2_falls_unbekannt" in result.dialog
    assert "_DECISIONS-chain" in result.dialog["frage_2_falls_unbekannt"]


def test_stufe4_dialog_for_unknown_role_offers_neubau(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("noch.nie.gesehene.rolle", store=store, home=home)
    assert result.stufe == Stufe.NICHT_GEFUNDEN
    assert "Neubau" in result.dialog["frage_2_falls_unbekannt"]


def test_stufe2_discovery_returns_proposal_not_autoconfirmed(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    discovery_root = tmp_path / "irgendwo"
    discovery_root.mkdir()
    (discovery_root / "MY-DECISIONS-REGISTER.md").write_text("x", encoding="utf-8")
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("decisions.ledger", store=store, home=home, discovery_roots=[discovery_root])
    assert result.stufe == Stufe.DISCOVERY_VORSCHLAG
    assert result.status == ResolutionStatus.PROPOSED
    assert len(result.kandidaten) == 1
    # Stufe-2-Fund darf NICHT automatisch im Speicher landen
    assert store.get("decisions.ledger") is None


def test_confirm_promotes_discovery_result_to_stufe0(tmp_path):
    store = UserSourceStore(tmp_path / "store.json")
    entry = confirm(
        "decisions.ledger",
        {"pfad": "/gefunden/MY-DECISIONS-REGISTER.md"},
        stufe_herkunft=2,
        bestaetigt_von="user",
        store=store,
    )
    assert entry.stufe == 0
    assert entry.herkunft == "discovery-bestaetigt"
    loaded = store.get("decisions.ledger")
    assert loaded is not None
    assert loaded.aktiv is True
    home = tmp_path / "home-unused"
    home.mkdir()
    result = resolve("decisions.ledger", store=store, home=home)
    assert result.stufe == Stufe.NUTZER_KONFIGURATION
    assert result.quelle["pfad"] == "/gefunden/MY-DECISIONS-REGISTER.md"


def test_adapter_role_without_scope_short_circuits_as_adapter_error(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("policy.registry", store=store, home=home)
    # kein scope uebergeben -> eigener, spezifischer Befund (Aufrufer-Fehler), NICHT
    # das generische "nichts gefunden" -- siehe advisor-Review 2026-08-15.
    assert result.stufe == Stufe.EIGENES_MODUL
    assert result.status == ResolutionStatus.ADAPTER_ERROR


def test_adapter_role_not_installed_short_circuits_distinctly(tmp_path, monkeypatch):
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: None)
    home = tmp_path / "home"
    home.mkdir()
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("policy.registry", store=store, home=home, scope="dev-hygiene")
    # "Modul vorhanden, CLI nicht aufrufbar" ist ein eigener Befund -- er faellt NICHT
    # still zu Stufe 2 durch (advisor-Review: "distinct result rather than silently
    # falling to Stufe 2").
    assert result.stufe == Stufe.EIGENES_MODUL
    assert result.status == ResolutionStatus.MODULE_PRESENT_NOT_CALLABLE
    assert "nicht auf PATH" in result.nachricht


def test_adapter_role_resolved_short_circuits_ladder(tmp_path, monkeypatch):
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: "/usr/bin/policy-registry")

    def _run(cmd, capture_output, text, timeout):
        class Proc:
            stdout = json.dumps({
                "status": "resolved",
                "selected": {"id": "P-001"},
                "candidates": [], "reason": None, "fallback": None,
            })
            stderr = ""
            returncode = 0
        return Proc()

    monkeypatch.setattr(pr_adapter.subprocess, "run", _run)
    home = tmp_path / "home"
    home.mkdir()
    store = UserSourceStore(tmp_path / "store.json")
    result = resolve("policy.registry", store=store, home=home, scope="dev-hygiene")
    assert result.stufe == Stufe.EIGENES_MODUL
    assert result.status == ResolutionStatus.RESOLVED
    assert result.quelle["selected"]["id"] == "P-001"


def test_stufe0_user_override_wins_even_for_adapter_role(tmp_path, monkeypatch):
    """Amendment 1 wortwoertlich: der Nutzer ueberschreibt auch ein Modul mit Adapter."""
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: "/usr/bin/policy-registry")
    store = UserSourceStore(tmp_path / "store.json")
    store.set(RoleEntry(
        rolle="policy.registry", aktiv=True,
        quelle={"pfad": "/mein/eigenes/policy-set.json"},
        stufe=0, bestaetigt_am=now_iso(), bestaetigt_von="user", herkunft="manuell",
    ))
    home = tmp_path / "home"
    home.mkdir()
    result = resolve("policy.registry", store=store, home=home, scope="dev-hygiene")
    assert result.stufe == Stufe.NUTZER_KONFIGURATION
    assert result.quelle["pfad"] == "/mein/eigenes/policy-set.json"
