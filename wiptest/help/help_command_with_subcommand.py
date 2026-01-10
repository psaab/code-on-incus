"""
Test help command with subcommand argument.

Expected:
- help <subcommand> shows subcommand help
"""

import subprocess


def test_help_command_with_subcommand(coi_binary):
    """Test that coi help <subcommand> shows subcommand help."""
    result = subprocess.run(
        [coi_binary, "help", "shell"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "shell" in result.stdout.lower()
    assert "usage:" in result.stdout.lower()
