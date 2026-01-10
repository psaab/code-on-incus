"""
Test version output is concise.

Expected:
- Version output is brief (not verbose help)
"""

import subprocess


def test_version_is_brief(coi_binary):
    """Test that version output is concise (not verbose help)."""
    result = subprocess.run([coi_binary, "--version"], capture_output=True, text=True, timeout=5)

    assert result.returncode == 0

    output = result.stdout + result.stderr
    lines = [line for line in output.split("\n") if line.strip()]

    # Version output should be brief (not more than a few lines)
    assert len(lines) <= 5, f"Version output should be brief, got {len(lines)} lines: {output}"
