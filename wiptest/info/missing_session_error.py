"""
Test info command error when session ID is missing.

Expected:
- Shows appropriate error or help when no session ID provided
"""

import subprocess


def test_info_without_session_id(coi_binary):
    """Test that info without session ID shows appropriate error."""
    result = subprocess.run([coi_binary, "info"], capture_output=True, text=True, timeout=5)

    # Should either show error or help
    # Exit code might be non-zero
    output = result.stdout + result.stderr

    # Should mention needing a session ID or show error
    assert (
        "session" in output.lower()
        or "usage" in output.lower()
        or "required" in output.lower()
        or "error" in output.lower()
    ), "Should indicate session ID is needed"
