"""
Test list command help functionality.

Expected:
- Help flag works and shows usage
"""

import subprocess


def test_list_help_flag(coi_binary):
    """Test that coi list --help shows help."""
    result = subprocess.run(
        [coi_binary, "list", "--help"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "list" in result.stdout.lower()
    assert "usage:" in result.stdout.lower() or "examples:" in result.stdout.lower()
