"""
Test clean command help shows available options.

Expected:
- Help mentions cleanup targets (containers, sessions, all)
"""

import subprocess


def test_clean_help_shows_options(coi_binary):
    """Test that clean help shows available options."""
    result = subprocess.run(
        [coi_binary, "clean", "--help"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    output = result.stdout.lower()

    # Should mention what can be cleaned
    assert "container" in output or "session" in output or "all" in output, (
        "Help should mention cleanup targets"
    )
