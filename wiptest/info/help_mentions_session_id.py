"""
Test info help mentions session ID parameter.

Expected:
- Help mentions session parameter requirement
"""

import subprocess


def test_info_help_mentions_session_id(coi_binary):
    """Test that info help mentions session ID parameter."""
    result = subprocess.run(
        [coi_binary, "info", "--help"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    output = result.stdout.lower()

    # Help should mention session
    assert "session" in output, "Help should mention session parameter"
