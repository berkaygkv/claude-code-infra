#!/usr/bin/env python3
"""
KH Bootstrap System: Initialize vault and config for new installations.

Usage:
    python scripts/bootstrap.py init --project myproject --vault /path/to/vault
    python scripts/bootstrap.py check
    python scripts/bootstrap.py show-config
    python scripts/bootstrap.py --test

Commands:
    init         Create vault structure and config file
    check        Validate current setup
    show-config  Display current configuration

Options:
    --project    Project name (lowercase, a-z/0-9/-, max 50 chars, starts with letter)
    --vault      Path to vault root (absolute, parent must exist, not inside kh/)
    --test       Run built-in tests
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================================
# Exceptions
# ============================================================================

class BootstrapError(Exception):
    """Base exception for bootstrap errors."""
    pass


class ConfigError(BootstrapError):
    """Config file related errors."""
    pass


class VaultError(BootstrapError):
    """Vault structure related errors."""
    pass


class ValidationError(BootstrapError):
    """Input validation errors."""
    pass


# ============================================================================
# Configuration
# ============================================================================

def get_kh_path() -> Path:
    """Get KH repository path (parent of scripts directory)."""
    return Path(__file__).parent.parent.resolve()


def get_config_path() -> Path:
    """Get path to config file."""
    return get_kh_path() / ".kh-config.json"


def get_templates_path() -> Path:
    """Get path to templates directory."""
    return get_kh_path() / "templates"


# ============================================================================
# Logging
# ============================================================================

def log_info(msg: str) -> None:
    """Log info message to stderr."""
    print(f"[INFO] {msg}", file=sys.stderr)


def log_warn(msg: str) -> None:
    """Log warning message to stderr."""
    print(f"[WARN] {msg}", file=sys.stderr)


def log_error(msg: str) -> None:
    """Log error message to stderr."""
    print(f"[ERROR] {msg}", file=sys.stderr)


def log_success(msg: str) -> None:
    """Log success message to stderr."""
    print(f"[OK] {msg}", file=sys.stderr)


# ============================================================================
# Validation
# ============================================================================

def validate_project_name(name: str) -> str:
    """Validate and normalize project name.

    Rules:
    - Lowercase letters, numbers, hyphens only
    - Must start with a letter
    - Max 50 characters
    - No consecutive hyphens

    Returns normalized name or raises ValidationError.
    """
    if not name:
        raise ValidationError("Project name is required")

    name = name.lower().strip()

    if len(name) > 50:
        raise ValidationError(f"Project name too long: {len(name)} chars (max 50)")

    if not re.match(r'^[a-z]', name):
        raise ValidationError(f"Project name must start with a letter: '{name}'")

    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        raise ValidationError(
            f"Project name can only contain lowercase letters, numbers, and hyphens: '{name}'"
        )

    if '--' in name:
        raise ValidationError(f"Project name cannot have consecutive hyphens: '{name}'")

    if name.endswith('-'):
        raise ValidationError(f"Project name cannot end with a hyphen: '{name}'")

    return name


def validate_vault_path(vault_path: str, kh_path: Path) -> Path:
    """Validate vault path.

    Rules:
    - Must be absolute path
    - Parent directory must exist (we create the vault dir)
    - Cannot be inside kh/ directory
    - Cannot be root or home directory

    Returns resolved Path or raises ValidationError.
    """
    if not vault_path:
        raise ValidationError("Vault path is required")

    path = Path(vault_path).resolve()

    if not path.is_absolute():
        raise ValidationError(f"Vault path must be absolute: '{vault_path}'")

    # Check not inside kh directory
    try:
        path.relative_to(kh_path)
        raise ValidationError(f"Vault path cannot be inside kh directory: '{vault_path}'")
    except ValueError:
        pass  # Good - path is not relative to kh_path

    # Check parent exists
    if not path.parent.exists():
        raise ValidationError(f"Parent directory does not exist: '{path.parent}'")

    # Sanity checks
    if path == Path("/") or path == Path.home():
        raise ValidationError(f"Vault path cannot be root or home directory: '{vault_path}'")

    return path


# ============================================================================
# Config Operations
# ============================================================================

def load_config() -> dict[str, Any]:
    """Load config from .kh-config.json.

    Raises ConfigError if file doesn't exist or is invalid.
    """
    config_path = get_config_path()

    if not config_path.exists():
        raise ConfigError(f"Config not found: {config_path}")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config: {e}")

    # Validate required keys
    required = ["vault_path", "vault_root", "kh_path", "project_name", "initialized"]
    missing = [k for k in required if k not in config]
    if missing:
        raise ConfigError(f"Missing required config keys: {missing}")

    return config


def save_config(config: dict[str, Any]) -> None:
    """Save config to .kh-config.json."""
    config_path = get_config_path()

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    log_success(f"Config saved: {config_path}")


def create_config(project_name: str, vault_root: Path) -> dict[str, Any]:
    """Create new config dictionary."""
    kh_path = get_kh_path()
    vault_path = vault_root / "notes"

    return {
        "vault_path": str(vault_path),
        "vault_root": str(vault_root),
        "kh_path": str(kh_path),
        "project_name": project_name,
        "initialized": datetime.now().isoformat()
    }


# ============================================================================
# Vault Operations
# ============================================================================

VAULT_DIRECTORIES = [
    "notes",
    "notes/Sessions",
    "notes/Sessions/transcripts",
    "notes/research",
    "notes/research/targets",
    "notes/research/outputs",
    "notes/templates",
    "notes/plans",
]

VAULT_FILES = [
    ("notes/locked.md", "locked.md.template"),
    ("notes/runbook.md", "runbook.md.template"),
    ("notes/overview.md", "overview.md.template"),
    ("notes/schemas.md", "schemas.md"),
]


def render_template(template_content: str, project_name: str) -> str:
    """Render template with placeholders replaced."""
    today = datetime.now().strftime("%Y-%m-%d")

    result = template_content.replace("{{PROJECT_NAME}}", project_name)
    result = result.replace("{{DATE}}", today)

    return result


def create_vault_structure(vault_root: Path, project_name: str) -> list[str]:
    """Create vault directory structure and files.

    Returns list of created paths.
    """
    templates_path = get_templates_path()
    created = []

    # Create directories
    for dir_path in VAULT_DIRECTORIES:
        full_path = vault_root / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(str(full_path))
            log_info(f"Created directory: {full_path}")
        else:
            log_info(f"Directory exists: {full_path}")

    # Create files from templates
    for vault_file, template_name in VAULT_FILES:
        full_path = vault_root / vault_file
        template_path = templates_path / template_name

        if full_path.exists():
            log_info(f"File exists (skipped): {full_path}")
            continue

        if not template_path.exists():
            log_warn(f"Template not found: {template_path}")
            continue

        template_content = template_path.read_text()
        rendered = render_template(template_content, project_name)
        full_path.write_text(rendered)
        created.append(str(full_path))
        log_success(f"Created file: {full_path}")

    return created


def create_obsidian_config(vault_root: Path) -> None:
    """Create minimal .obsidian config (optional)."""
    obsidian_path = vault_root / ".obsidian"

    if obsidian_path.exists():
        log_info(f"Obsidian config exists: {obsidian_path}")
        return

    obsidian_path.mkdir(exist_ok=True)

    # Minimal app.json
    app_config = {
        "alwaysUpdateLinks": True,
        "newLinkFormat": "relative",
        "useMarkdownLinks": False
    }

    (obsidian_path / "app.json").write_text(json.dumps(app_config, indent=2))
    log_success(f"Created Obsidian config: {obsidian_path}")


# ============================================================================
# Commands
# ============================================================================

def cmd_init(args: argparse.Namespace) -> int:
    """Initialize vault and config."""
    kh_path = get_kh_path()

    # Validate inputs
    try:
        project_name = validate_project_name(args.project)
        vault_root = validate_vault_path(args.vault, kh_path)
    except ValidationError as e:
        log_error(str(e))
        return 1

    # Check if already initialized
    config_path = get_config_path()
    if config_path.exists() and not args.force:
        log_error(f"Already initialized. Use --force to reinitialize.")
        log_info(f"Config: {config_path}")
        return 1

    log_info(f"Initializing KH for project: {project_name}")
    log_info(f"Vault root: {vault_root}")

    # Create vault structure
    try:
        # Create vault root if needed
        if not vault_root.exists():
            vault_root.mkdir(parents=True)
            log_success(f"Created vault root: {vault_root}")

        # Create directory structure and files
        created = create_vault_structure(vault_root, project_name)

        # Create optional Obsidian config
        if not args.no_obsidian:
            create_obsidian_config(vault_root)

    except Exception as e:
        log_error(f"Failed to create vault: {e}")
        return 1

    # Create and save config
    config = create_config(project_name, vault_root)
    save_config(config)

    print(f"\nInitialization complete!")
    print(f"  Project: {project_name}")
    print(f"  Vault: {vault_root}")
    print(f"  Config: {config_path}")
    print(f"\nCreated {len(created)} items.")
    print(f"\nNext steps:")
    print(f"  1. Open vault in Obsidian: {vault_root}")
    print(f"  2. Start a session: /begin")

    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """Check current setup validity."""
    issues = []

    # Check config
    try:
        config = load_config()
        log_success(f"Config loaded: {get_config_path()}")
    except ConfigError as e:
        log_error(str(e))
        return 1

    # Validate paths exist
    vault_path = Path(config["vault_path"])
    vault_root = Path(config["vault_root"])
    kh_path = Path(config["kh_path"])

    if not vault_root.exists():
        issues.append(f"Vault root missing: {vault_root}")
    else:
        log_success(f"Vault root exists: {vault_root}")

    if not vault_path.exists():
        issues.append(f"Vault notes missing: {vault_path}")
    else:
        log_success(f"Vault notes exists: {vault_path}")

    if not kh_path.exists():
        issues.append(f"KH path missing: {kh_path}")
    else:
        log_success(f"KH path exists: {kh_path}")

    # Check required directories
    for dir_path in VAULT_DIRECTORIES:
        full_path = vault_root / dir_path
        if not full_path.exists():
            issues.append(f"Directory missing: {full_path}")
        else:
            log_success(f"Directory OK: {dir_path}")

    # Check required files
    for vault_file, _ in VAULT_FILES:
        full_path = vault_root / vault_file
        if not full_path.exists():
            issues.append(f"File missing: {full_path}")
        else:
            log_success(f"File OK: {vault_file}")

    # Report
    if issues:
        print(f"\nFound {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    else:
        print(f"\nAll checks passed!")
        return 0


def cmd_show_config(args: argparse.Namespace) -> int:
    """Display current configuration."""
    try:
        config = load_config()
    except ConfigError as e:
        log_error(str(e))
        return 1

    print(json.dumps(config, indent=2))
    return 0


# ============================================================================
# Tests
# ============================================================================

def run_tests() -> int:
    """Run built-in tests."""
    import tempfile

    passed = 0
    failed = 0

    def test(name: str, fn) -> None:
        nonlocal passed, failed
        try:
            fn()
            print(f"  PASS: {name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {name} - {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR: {name} - {e}")
            failed += 1

    print("Running tests...\n")

    # Test validate_project_name
    def test_project_name_valid():
        assert validate_project_name("myproject") == "myproject"
        assert validate_project_name("my-project") == "my-project"
        assert validate_project_name("project123") == "project123"
        assert validate_project_name("MyProject") == "myproject"  # Lowercased

    def test_project_name_invalid():
        try:
            validate_project_name("123project")
            assert False, "Should reject names starting with number"
        except ValidationError:
            pass

        try:
            validate_project_name("my_project")
            assert False, "Should reject underscores"
        except ValidationError:
            pass

        try:
            validate_project_name("my--project")
            assert False, "Should reject consecutive hyphens"
        except ValidationError:
            pass

        try:
            validate_project_name("")
            assert False, "Should reject empty"
        except ValidationError:
            pass

    def test_project_name_max_length():
        long_name = "a" * 50
        assert validate_project_name(long_name) == long_name

        try:
            validate_project_name("a" * 51)
            assert False, "Should reject >50 chars"
        except ValidationError:
            pass

    # Test validate_vault_path
    def test_vault_path_valid():
        with tempfile.TemporaryDirectory() as tmpdir:
            kh_path = Path(tmpdir) / "kh"
            kh_path.mkdir()

            vault_path = Path(tmpdir) / "vault"
            result = validate_vault_path(str(vault_path), kh_path)
            assert result == vault_path

    def test_vault_path_invalid():
        kh_path = get_kh_path()

        try:
            validate_vault_path(str(kh_path / "inside"), kh_path)
            assert False, "Should reject paths inside kh"
        except ValidationError:
            pass

        try:
            validate_vault_path("relative/path", kh_path)
            assert False, "Should reject relative paths"
        except ValidationError:
            pass

        try:
            validate_vault_path("/nonexistent/parent/vault", kh_path)
            assert False, "Should reject non-existent parent"
        except ValidationError:
            pass

    # Test vault creation (idempotency)
    def test_vault_creation():
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_root = Path(tmpdir) / "test-vault"
            vault_root.mkdir()

            # First run
            created1 = create_vault_structure(vault_root, "test")
            assert len(created1) > 0

            # Second run (idempotent - nothing new created)
            created2 = create_vault_structure(vault_root, "test")
            assert len(created2) == 0

    def test_template_rendering():
        template = "Project: {{PROJECT_NAME}}\nDate: {{DATE}}"
        rendered = render_template(template, "myproject")
        assert "Project: myproject" in rendered
        assert "{{PROJECT_NAME}}" not in rendered
        assert "{{DATE}}" not in rendered

    # Run all tests
    test("validate_project_name valid", test_project_name_valid)
    test("validate_project_name invalid", test_project_name_invalid)
    test("validate_project_name max length", test_project_name_max_length)
    test("validate_vault_path valid", test_vault_path_valid)
    test("validate_vault_path invalid", test_vault_path_invalid)
    test("vault creation idempotency", test_vault_creation)
    test("template rendering", test_template_rendering)

    print(f"\nResults: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="KH Bootstrap System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run built-in tests"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize vault and config")
    init_parser.add_argument(
        "--project", "-p",
        required=True,
        help="Project name"
    )
    init_parser.add_argument(
        "--vault", "-v",
        required=True,
        help="Path to vault root"
    )
    init_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force reinitialize even if config exists"
    )
    init_parser.add_argument(
        "--no-obsidian",
        action="store_true",
        help="Skip creating .obsidian config"
    )

    # check command
    subparsers.add_parser("check", help="Validate current setup")

    # show-config command
    subparsers.add_parser("show-config", help="Display configuration")

    args = parser.parse_args()

    if args.test:
        sys.exit(run_tests())

    if args.command == "init":
        sys.exit(cmd_init(args))
    elif args.command == "check":
        sys.exit(cmd_check(args))
    elif args.command == "show-config":
        sys.exit(cmd_show_config(args))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
