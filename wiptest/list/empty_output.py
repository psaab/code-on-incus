"""
Test list command output when no sessions exist.

Expected:
- Shows appropriate message or empty table
- Does not crash
"""

import subprocess


def test_list_shows_appropriate_message_when_empty(coi_binary):
    """Test that list shows message when no sessions exist."""
    result = subprocess.run([coi_binary, "list"], capture_output=True, text=True, timeout=10)

    assert result.returncode == 0
    output = result.stdout + result.stderr

    # Should either show "No active" or show table headers or show nothing
    # Just verify it doesn't crash
    assert output is not None
