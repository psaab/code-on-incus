"""
Test that clean command does NOT remove running containers.

Flow:
1. Get list of running claude containers before clean
2. Run coi clean --force
3. Verify all running containers still exist

Expected:
- Running containers are preserved
- Clean operation succeeds
"""

import subprocess


def test_clean_preserves_running_containers(coi_binary):
    """Test that clean does NOT remove running containers."""
    # Get list of running claude containers before clean
    list_before = subprocess.run(
        ["incus", "list", "claude-", "--format=csv"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    running_containers_before = [
        line.split(",")[0]
        for line in list_before.stdout.strip().split("\n")
        if line and "RUNNING" in line
    ]

    # Run clean
    clean_result = subprocess.run(
        [coi_binary, "clean", "--force"], capture_output=True, text=True, timeout=30
    )

    assert clean_result.returncode == 0

    # Get list of running containers after clean
    list_after = subprocess.run(
        ["incus", "list", "claude-", "--format=csv"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    running_containers_after = [
        line.split(",")[0]
        for line in list_after.stdout.strip().split("\n")
        if line and "RUNNING" in line
    ]

    # All previously running containers should still be running
    for container in running_containers_before:
        assert container in running_containers_after, (
            f"Running container {container} should not be removed"
        )
