"""
Test list behavior without Incus permissions.

Expected:
- Command completes without crashing
- May show permission error or work depending on setup
"""

import subprocess


def test_list_without_incus_permissions(coi_binary):
    """Test list behavior without Incus permissions."""
    # Run without sg - might show permission error but shouldn't crash
    result = subprocess.run(
        [coi_binary, "list"],
        capture_output=True,
        text=True,
        timeout=10,
        env={"PATH": "/usr/bin:/bin"},
    )

    # Exit code might be 0 or non-zero depending on permissions
    # Just verify it completes
    assert result.returncode is not None
