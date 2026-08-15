from source_resolver.store import RoleEntry, UserSourceStore, now_iso


def make_store(tmp_path):
    return UserSourceStore(tmp_path / "config.json")


def test_get_on_empty_store_returns_none(tmp_path):
    store = make_store(tmp_path)
    assert store.get("decisions.ledger") is None


def test_set_and_get_roundtrip(tmp_path):
    store = make_store(tmp_path)
    entry = RoleEntry(
        rolle="decisions.ledger",
        aktiv=True,
        quelle={"pfad": "/x/DECISIONS.md"},
        stufe=0,
        bestaetigt_am=now_iso(),
        bestaetigt_von="user",
        herkunft="manuell",
    )
    store.set(entry)
    loaded = store.get("decisions.ledger")
    assert loaded is not None
    assert loaded.quelle == {"pfad": "/x/DECISIONS.md"}
    assert loaded.aktiv is True


def test_deactivate_keeps_entry_visible_but_inactive(tmp_path):
    store = make_store(tmp_path)
    entry = RoleEntry(
        rolle="user.model", aktiv=True, quelle={}, stufe=0,
        bestaetigt_am=now_iso(), bestaetigt_von="user", herkunft="manuell",
    )
    store.set(entry)
    assert store.deactivate("user.model") is True
    loaded = store.get("user.model")
    assert loaded is not None
    assert loaded.aktiv is False


def test_deactivate_unknown_role_returns_false(tmp_path):
    store = make_store(tmp_path)
    assert store.deactivate("no.such.role") is False


def test_list_roles_returns_all_entries(tmp_path):
    store = make_store(tmp_path)
    for rolle in ("policy.registry", "decisions.ledger"):
        store.set(RoleEntry(
            rolle=rolle, aktiv=True, quelle={}, stufe=0,
            bestaetigt_am=now_iso(), bestaetigt_von="user", herkunft="manuell",
        ))
    roles = store.list_roles()
    assert set(roles.keys()) == {"policy.registry", "decisions.ledger"}


def test_corrupted_store_raises_explicit_error(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{not valid json", encoding="utf-8")
    store = UserSourceStore(path)
    try:
        store.get("policy.registry")
        assert False, "expected ValueError"
    except ValueError as error:
        assert "beschaedigt" in str(error)
