"""
Test version output contains a version number.

Expected:
- Version number follows X.Y.Z pattern
"""

import re
import subprocess


def test_version_shows_number(coi_binary):
    """Test that version output contains a version number."""
    result = subprocess.run([coi_binary, "--version"], capture_output=True, text=True, timeout=5)

    assert result.returncode == 0

    output = result.stdout + result.stderr

    # Should contain something that looks like a version number (e.g., 0.1.0)
    # Match patterns like X.Y.Z or vX.Y.Z
    version_pattern = r"\d+\.\d+\.\d+"
    assert re.search(version_pattern, output), (
        f"Expected version number pattern (X.Y.Z) in output, got: {output}"
    )
