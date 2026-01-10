"""
Test version flag displays version information.

Expected:
- Version information is displayed
- Exit code is 0
"""

import subprocess


def test_version_flag(coi_binary):
    """Test that coi --version displays version information."""
    result = subprocess.run([coi_binary, "--version"], capture_output=True, text=True, timeout=5)

    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"

    # Version can be in stdout or stderr
    output = result.stdout + result.stderr
    output_lower = output.lower()

    # Should contain version information
    assert "version" in output_lower or "coi" in output_lower or "0." in output, (
        f"Expected version info in output, got: {output}"
    )
