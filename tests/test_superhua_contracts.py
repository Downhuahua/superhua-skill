from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILL = REPO_ROOT / "skills" / "superhua"
INSTALLED_SKILL = Path.home() / ".codex" / "skills" / "superhua"
README = REPO_ROOT / "README.md"

TRANSIENT_DIRS = {"__pycache__", ".pytest_cache", "_backups", "output"}
TRANSIENT_SUFFIXES = {".pyc", ".pyo"}

REQUIRED_AGENT_PROMPTS = [
    "task-router.md",
    "lite-executor.md",
    "standard-executor.md",
    "proposal-writer.md",
    "proposal-reviewer.md",
    "design-writer.md",
    "design-reviewer.md",
    "detailed-design-writer.md",
    "detailed-design-reviewer.md",
    "task-writer.md",
    "task-reviewer.md",
    "prompt-writer.md",
    "prompt-reviewer.md",
    "spec-writer.md",
    "planner.md",
    "plan-reviewer.md",
    "implementer.md",
    "spec-reviewer.md",
    "code-reviewer.md",
]

REQUIRED_UPSTREAM_PATHS = [
    "references/upstream-superteam/skills/planning/SKILL.md",
    "references/upstream-superteam/skills/executing/SKILL.md",
    "references/upstream-superteam/skills/black-box-testing/SKILL.md",
    "references/upstream-superteam/skills/hands-off-issue-handling/SKILL.md",
    "references/upstream-superteam/agents/planner.md",
    "references/upstream-superteam/agents/plan-reviewer.md",
    "references/upstream-superteam/agents/implementer.md",
    "references/upstream-superteam/agents/spec-reviewer.md",
    "references/upstream-superteam/agents/code-reviewer.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _relative_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in TRANSIENT_DIRS for part in rel.parts):
            continue
        if path.suffix in TRANSIENT_SUFFIXES:
            continue
        files[rel.as_posix()] = path
    return files


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def test_required_superhua_agent_prompts_exist() -> None:
    for name in REQUIRED_AGENT_PROMPTS:
        assert (SOURCE_SKILL / "agents" / name).is_file(), name


def test_workflow_prompt_file_references_exist_in_source_and_install() -> None:
    workflow = _read(SOURCE_SKILL / "references" / "workflow.md")
    refs = sorted(
        set(
            re.findall(
                r"Prompt file: C:/Users/HUA/\.codex/skills/superhua/(agents/[^\s`]+)",
                workflow,
            )
        )
    )
    assert refs

    for rel in refs:
        assert (SOURCE_SKILL / rel).is_file(), rel

    if not INSTALLED_SKILL.exists():
        pytest.skip(f"installed SuperHUA package is absent: {INSTALLED_SKILL}")

    for rel in refs:
        assert (INSTALLED_SKILL / rel).is_file(), rel


def test_upstream_reference_paths_exist_for_stage6_engine() -> None:
    workflow = _read(SOURCE_SKILL / "references" / "workflow.md")
    skill = _read(SOURCE_SKILL / "SKILL.md")

    for rel in REQUIRED_UPSTREAM_PATHS:
        assert rel in workflow or rel in skill, rel
        assert (SOURCE_SKILL / rel).is_file(), rel

    if not INSTALLED_SKILL.exists():
        pytest.skip(f"installed SuperHUA package is absent: {INSTALLED_SKILL}")

    for rel in REQUIRED_UPSTREAM_PATHS:
        assert (INSTALLED_SKILL / rel).is_file(), rel


def test_mode_markers_remain_in_skill_and_workflow_contracts() -> None:
    skill = _read(SOURCE_SKILL / "SKILL.md")
    workflow = _read(SOURCE_SKILL / "references" / "workflow.md")

    for mode in ["vibe-lite", "vibe-standard", "spec-full"]:
        assert mode in skill
        assert mode in workflow


def test_spec_writer_has_deterministic_blocking_output_contract() -> None:
    text = _read(SOURCE_SKILL / "agents" / "spec-writer.md")

    assert "Spec issues path" in text
    assert "Output files:\n- <spec issues path>" in text
    assert "Status: Blocked" in text
    assert "Status: Needs User" in text
    assert "do not write the provided spec path" in text


def test_stage6_contract_stops_on_spec_issues_without_valid_spec() -> None:
    skill = _read(SOURCE_SKILL / "SKILL.md")
    workflow = _read(SOURCE_SKILL / "references" / "workflow.md")

    for text in [skill, workflow]:
        compact = re.sub(r"\s+", " ", text)
        assert "RUN/spec-issues.md" in text
        assert "Status: Blocked" in text
        assert "Status: Needs User" in text
        assert "missing or stale `RUN/spec.md`" in text
        assert "Do not dispatch planner" in compact or "must not dispatch planner" in compact


def test_readme_documents_windows_utf8_validation_and_license_risk() -> None:
    text = _read(README)

    assert "$env:PYTHONUTF8='1'" in text
    assert "$env:USERPROFILE" in text
    assert "$PWD\\skills\\superhua" in text
    assert "C:\\Users\\HUA" not in text
    assert "quick_validate.py" in text
    assert "public redistribution" in text
    assert "not locally resolved" in text or "requires upstream rights confirmation" in text


def test_source_and_installed_superhua_packages_are_in_safe_parity() -> None:
    if not INSTALLED_SKILL.exists():
        pytest.skip(f"installed SuperHUA package is absent: {INSTALLED_SKILL}")

    source_files = _relative_files(SOURCE_SKILL)
    installed_files = _relative_files(INSTALLED_SKILL)

    assert set(source_files) == set(installed_files)
    for rel, source_path in source_files.items():
        assert _sha256(source_path) == _sha256(installed_files[rel]), rel
