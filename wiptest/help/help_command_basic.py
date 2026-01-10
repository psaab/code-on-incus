"""
Test help subcommand basic functionality.

Expected:
- help command works (alternative to --help)
"""

import subprocess


def test_help_command(coi_binary):
    """Test that coi help shows help text."""
    result = subprocess.run([coi_binary, "help"], capture_output=True, text=True, timeout=5)

    assert result.returncode == 0
    assert "claude-on-incus" in result.stdout.lower()
    assert "usage:" in result.stdout.lower() or "available commands" in result.stdout.lower()
