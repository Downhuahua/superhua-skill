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

HARNESS_PATTERNS = [
    "pipeline",
    "fan-out-fan-in",
    "expert-pool",
    "producer-reviewer",
    "supervisor",
    "hierarchical",
    "none",
]

INVOCATION_STRATEGIES = [
    "single-agent",
    "parallel-subagents",
    "serial-review-loop",
    "full-superteam",
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
                r"Prompt file: <installed SuperHUA skill root>/(agents/[^\s`]+)",
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


def test_router_keeps_known_skill_patches_lightweight() -> None:
    skill = _read(SOURCE_SKILL / "SKILL.md")
    workflow = _read(SOURCE_SKILL / "references" / "workflow.md")
    router = _read(SOURCE_SKILL / "agents" / "task-router.md")
    readme = _read(README)

    for text in [skill, router]:
        assert "bounded skill-maintenance patches" in text
        assert re.search(r"up to\s+five", text)
        assert re.search(
            r"Do not route a skill update\s+to `vibe-standard` solely",
            text,
        )
        assert "半小时" in text
        assert "别跑重流程" in text

    assert "default for known small skill-maintenance patches" in workflow
    assert "one child agent, one small patch, and one targeted verification" in workflow
    assert "known small skill-maintenance patches" in readme


def test_harness_architecture_selector_contract_exists() -> None:
    skill = _read(SOURCE_SKILL / "SKILL.md")
    workflow = _read(SOURCE_SKILL / "references" / "workflow.md")
    router = _read(SOURCE_SKILL / "agents" / "task-router.md")
    readme = _read(README)
    adaptation_path = SOURCE_SKILL / "references" / "harness-adaptation.md"
    adaptation = _read(adaptation_path)

    assert adaptation_path.is_file()
    for text in [skill, workflow, router, readme, adaptation]:
        assert "Harness pattern" in text
        assert "Invocation strategy" in text

    for pattern in HARNESS_PATTERNS:
        assert pattern in adaptation
        assert pattern in router

    for strategy in INVOCATION_STRATEGIES:
        assert strategy in adaptation
        assert strategy in router

    assert "Known issue, known files, known checks" in adaptation
    assert "Do not import Harness's full team mode by" in adaptation
    assert "does not import Harness's full team mode by" in workflow


def test_checked_in_skill_has_no_user_specific_install_paths() -> None:
    checked_files = [
        path
        for path in SOURCE_SKILL.rglob("*")
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}
    ]

    for path in checked_files:
        text = _read(path)
        assert "C:/Users/HUA" not in text, path
        assert "C:\\Users\\HUA" not in text, path


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
