"""Automated contract tests for repository hygiene, PEP 621 metadata, and CI/Security compliance."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

import source_resolver
from source_resolver.ladder import ResolutionStatus, Stufe

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_version_parity():
    """Verify that version strings across package, pyproject.toml, and ellmos-module manifest match."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file(), "pyproject.toml must exist"

    with pyproject_path.open("rb") as f:
        pyproject = tomllib.load(f)

    project_version = pyproject["project"]["version"]
    assert source_resolver.__version__ == project_version, "source_resolver.__version__ must match pyproject.toml"
    assert source_resolver.__version__ == "0.1.4", "Expected version 0.1.4"

    manifest_path = REPO_ROOT / "ellmos-module.v2.json"
    assert manifest_path.is_file(), "ellmos-module.v2.json must exist"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest.get("version") == project_version, "ellmos-module.v2.json version must match pyproject.toml"


def test_pep621_pyproject_structure():
    """Verify PEP 621 compliance, URLs, classifiers, and tool options."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        pyproject = tomllib.load(f)

    project = pyproject["project"]
    assert project["name"] == "source-resolver"
    assert project["readme"] == "README.md"
    assert project["requires-python"] == ">=3.10"
    assert project["license"] == {"text": "MIT"}
    assert project.get("license-files") == ["LICENSE", "THIRD_PARTY_LICENSES.md"]

    # URLs
    urls = project["urls"]
    assert "Homepage" in urls
    assert "Repository" in urls
    assert "Documentation" in urls
    assert "Issues" in urls
    assert "Changelog" in urls
    assert "Security" in urls

    # Classifiers
    classifiers = project["classifiers"]
    expected_classifiers = [
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ]
    for c in expected_classifiers:
        assert c in classifiers, f"Missing expected classifier: {c}"

    # Dependencies & tool configuration
    opt_deps = project["optional-dependencies"]
    assert "dev" in opt_deps and any("pytest" in d for d in opt_deps["dev"])
    assert "test" in opt_deps and any("pytest" in d for d in opt_deps["test"])

    pytest_opts = pyproject["tool"]["pytest"]["ini_options"]
    assert "-ra" in pytest_opts.get("addopts", "")
    assert "-v" in pytest_opts.get("addopts", "")

    ruff_opts = pyproject["tool"]["ruff"]
    assert ruff_opts.get("target-version") == "py310"
    assert ruff_opts.get("line-length") == 120


def test_gitignore_hygiene_patterns():
    """Verify that .gitignore guards against multi-host conflicts, system locks, and build artifacts."""
    gitignore_path = REPO_ROOT / ".gitignore"
    assert gitignore_path.is_file(), ".gitignore must exist"
    content = gitignore_path.read_text(encoding="utf-8")

    # Multi-host sync conflicts
    assert "*-conflict-*" in content
    assert "*-ASUS-GEI.*" in content
    assert "*-WORKSTATION-LG.*" in content
    assert "Thumbs.db" in content
    assert "desktop.ini" in content

    # System locks
    assert "LOCK" in content
    assert "LOCK.*" in content
    assert "*.lock" in content
    assert "LOCK*.txt" in content

    # Build and test artifacts
    assert ".pytest_cache/" in content
    assert ".ruff_cache/" in content
    assert "*.egg-info/" in content
    assert "__pycache__/" in content
    assert ".coverage" in content


def test_ci_workflows_contract():
    """Verify GitHub Actions CI matrix specification."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_path.is_file(), ".github/workflows/ci.yml must exist"
    content = ci_path.read_text(encoding="utf-8")

    # Triggers & Permissions
    assert "push:" in content
    assert "pull_request:" in content
    assert "workflow_dispatch:" in content
    assert "contents: read" in content
    assert "cancel-in-progress: true" in content

    # Matrix
    assert "ubuntu-latest" in content
    assert "windows-latest" in content
    assert "macos-latest" in content
    for py in ["3.10", "3.11", "3.12", "3.13"]:
        assert f'"{py}"' in content or f"'{py}'" in content or f" {py}" in content

    # Test execution steps
    assert "ruff check" in content
    assert "compileall" in content
    assert "pytest" in content


def test_stale_workflow_contract():
    """Verify GitHub Actions Stale workflow specification."""
    stale_path = REPO_ROOT / ".github" / "workflows" / "stale.yml"
    assert stale_path.is_file(), ".github/workflows/stale.yml must exist"
    content = stale_path.read_text(encoding="utf-8")

    assert "actions/stale@v9" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content
    assert "days-before-stale:" in content
    assert "days-before-close:" in content


def test_security_policy_contract():
    """Verify SECURITY.md presence, bilingual coverage, SLA definitions, and reporting channels."""
    security_path = REPO_ROOT / "SECURITY.md"
    assert security_path.is_file(), "SECURITY.md must exist"
    content = security_path.read_text(encoding="utf-8")

    # SLA requirements
    assert "48 hours" in content
    assert "5 business days" in content
    assert "48 Stunden" in content
    assert "5 Werktagen" in content

    # Reporting email contacts
    assert "security@open-bricks.org" in content
    assert "security@ellmos.ai" in content
    assert "lukas@open-bricks.org" in content

    # Architectural invariant coverage
    assert "Local-First" in content or "Local-first" in content or "local" in content.lower()
    assert "Zero Network Egress" in content or "Zero-Network-Egress" in content


def test_bilingual_readme_contract():
    """Verify README.md and README_de.md existence, banner linkage, and mutual references."""
    readme_en = REPO_ROOT / "README.md"
    readme_de = REPO_ROOT / "README_de.md"

    assert readme_en.is_file(), "README.md must exist"
    assert readme_de.is_file(), "README_de.md must exist"

    text_en = readme_en.read_text(encoding="utf-8")
    text_de = readme_de.read_text(encoding="utf-8")

    assert ("assets/banner.gif" in text_en or "assets/banner.png" in text_en), "README.md must link to banner asset"
    assert ("assets/banner.gif" in text_de or "assets/banner.png" in text_de), "README_de.md must link to banner asset"

    assert "README_de.md" in text_en, "README.md should link to German version"
    assert "README.md" in text_de, "README_de.md should link to English version"


def test_todo_and_license_inventory_contract():
    """Verify TODO.md with STATUS table, THIRD_PARTY_LICENSES.md, and PEP 639 metadata."""
    todo_path = REPO_ROOT / "TODO.md"
    assert todo_path.is_file(), "TODO.md must exist"
    todo_text = todo_path.read_text(encoding="utf-8")
    assert "## STATUS" in todo_text, "TODO.md must contain ## STATUS table"
    assert "READY" in todo_text, "TODO.md must reflect READY state"

    tpl_path = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    assert tpl_path.is_file(), "THIRD_PARTY_LICENSES.md must exist"
    tpl_text = tpl_path.read_text(encoding="utf-8")
    assert "Runtime Dependencies" in tpl_text
    assert "Zero-Copyleft" in tpl_text



def test_architecture_contract():
    """Verify ARCHITECTURE.md existence, sequence diagram presence, and diagram syntax integrity."""
    arch_path = REPO_ROOT / "ARCHITECTURE.md"
    assert arch_path.is_file(), "ARCHITECTURE.md must exist"

    arch_text = arch_path.read_text(encoding="utf-8")
    assert "flowchart TD" in arch_text, "ARCHITECTURE.md must contain flowchart diagram"
    assert "sequenceDiagram" in arch_text, "ARCHITECTURE.md must contain sequence diagram"

    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")
    assert "ARCHITECTURE.md" in readme_en, "README.md must link to ARCHITECTURE.md"
    assert "ARCHITECTURE.md" in readme_de, "README_de.md must link to ARCHITECTURE.md"
    assert "sequenceDiagram" in readme_en, "README.md must include sequence diagram"
    assert "sequenceDiagram" in readme_de, "README_de.md must include sequence diagram"


def test_contract_version_invariants():
    """Verify library public contract invariants and Stufe enumeration."""
    assert source_resolver.CONTRACT_VERSION == "1"
    assert "CONTRACT_VERSION" in source_resolver.__all__

    assert Stufe.NUTZER_KONFIGURATION == 0
    assert Stufe.EIGENES_MODUL == 1
    assert Stufe.DISCOVERY_VORSCHLAG == 2
    assert Stufe.FREMDANBIETER == 3
    assert Stufe.NICHT_GEFUNDEN == 4

    assert ResolutionStatus.RESOLVED == "resolved"
    assert ResolutionStatus.PROPOSED == "proposed"
    assert ResolutionStatus.NOT_FOUND == "not_found"
    assert ResolutionStatus.ADAPTER_ERROR == "adapter_error"
    assert ResolutionStatus.MODULE_PRESENT_NOT_CALLABLE == "module_present_not_callable"
    assert ResolutionStatus.NO_FOREIGN_PROVIDERS == "no_foreign_providers"
