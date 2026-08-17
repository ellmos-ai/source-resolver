import json

from source_resolver.cli import main


def test_cli_list_roles_empty_store_returns_zero(tmp_path, capsys):
    store_path = tmp_path / "config.json"
    rc = main(["--store", str(store_path), "list-roles"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out == {}


def test_cli_confirm_then_resolve_via_stufe0(tmp_path, capsys):
    store_path = tmp_path / "config.json"
    quelle = {"pfad": "/x/DECISIONS.md"}
    quelle_file = tmp_path / "quelle.json"
    quelle_file.write_text(json.dumps(quelle), encoding="utf-8")

    rc = main(["--store", str(store_path), "confirm", "decisions.ledger", str(quelle_file)])
    assert rc == 0
    capsys.readouterr()

    fake_home = tmp_path / "home"
    fake_home.mkdir()
    rc = main(["--store", str(store_path), "resolve", "decisions.ledger", "--home", str(fake_home)])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["stufe_name"] == "NUTZER_KONFIGURATION"
    assert out["quelle"]["pfad"] == "/x/DECISIONS.md"


def test_cli_check_pointer_missing_returns_exit_1(tmp_path, capsys):
    rc = main(["check-pointer", str(tmp_path / "does-not-exist")])
    assert rc == 1
    out = json.loads(capsys.readouterr().out)
    assert out["exists"] is False


def test_cli_check_pointer_existing_returns_exit_0(tmp_path, capsys):
    target = tmp_path / "here"
    target.mkdir()
    rc = main(["check-pointer", str(target)])
    assert rc == 0
