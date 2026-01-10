"""
Test completion command help flag.

Expected:
- Help flag works and shows usage
"""

import subprocess


def test_completion_help_flag(coi_binary):
    """Test that coi completion --help shows help."""
    result = subprocess.run(
        [coi_binary, "completion", "--help"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "completion" in result.stdout.lower()
    assert "usage:" in result.stdout.lower() or "shell" in result.stdout.lower()
