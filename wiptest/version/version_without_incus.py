"""
Test version works without Incus access.

Expected:
- Version displays even without Incus daemon
"""

import subprocess


def test_version_without_incus_access(coi_binary):
    """Test that version works even without Incus daemon access."""
    result = subprocess.run(
        [coi_binary, "--version"],
        capture_output=True,
        text=True,
        timeout=5,
        env={"PATH": "/usr/bin:/bin"},  # Minimal environment
    )

    assert result.returncode == 0
    output = result.stdout + result.stderr
    assert len(output.strip()) > 0, "Version output should not be empty"
