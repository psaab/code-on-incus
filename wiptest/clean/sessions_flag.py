"""
Test that clean --sessions flag works.

Expected:
- Sessions flag executes without error
- Command completes successfully
"""

import subprocess


def test_clean_sessions_flag(coi_binary):
    """Test that clean --sessions flag works."""
    result = subprocess.run(
        [coi_binary, "clean", "--sessions", "--force"],
        capture_output=True,
        text=True,
        timeout=30,
    )

    # Should complete without error
    assert result.returncode == 0, f"Clean sessions failed: {result.stderr}"
