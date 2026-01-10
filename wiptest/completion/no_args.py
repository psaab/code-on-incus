"""
Test completion behavior without shell argument.

Expected:
- Shows help or error about missing shell
"""

import subprocess


def test_completion_without_shell_shows_help(coi_binary):
    """Test that completion without shell argument shows help."""
    result = subprocess.run([coi_binary, "completion"], capture_output=True, text=True, timeout=5)

    output = result.stdout + result.stderr

    # Should show help or error about missing shell
    assert "usage:" in output.lower() or "shell" in output.lower() or "bash" in output.lower(), (
        "Should show usage or mention shell types"
    )
