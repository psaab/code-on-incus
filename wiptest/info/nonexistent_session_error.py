"""
Test info command error when session doesn't exist.

Expected:
- Shows appropriate error for non-existent session
"""

import subprocess


def test_info_with_nonexistent_session(coi_binary):
    """Test info with a non-existent session ID."""
    result = subprocess.run(
        [coi_binary, "info", "nonexistent-session-12345"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    # Should show error about session not found
    output = result.stdout + result.stderr

    # Should mention not found or error
    assert (
        "not found" in output.lower()
        or "error" in output.lower()
        or "does not exist" in output.lower()
    ), "Should indicate session not found"
