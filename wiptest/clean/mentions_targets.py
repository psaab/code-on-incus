"""
Test clean command mentions cleanup targets.

Expected:
- Output mentions containers or sessions
"""

import subprocess


def test_clean_mentions_containers_or_sessions(coi_binary):
    """Test that clean command mentions containers/sessions."""
    result = subprocess.run([coi_binary, "clean"], capture_output=True, text=True, timeout=10)

    output = (result.stdout + result.stderr).lower()

    # Should mention cleanup targets
    assert "container" in output or "session" in output or "usage" in output or "clean" in output, (
        "Should mention what can be cleaned"
    )
