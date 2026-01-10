"""
Integration tests for container CLI commands.

Tests:
- coi container launch
- coi container start/stop
- coi container delete
- coi container exec
- coi container exists/running
- coi container mount
"""

import subprocess
import time


def test_container_launch_persistent(coi_binary, cleanup_containers):
    """Test launching a persistent container."""
    container_name = "coi-test-launch-persistent"

    # Launch persistent container
    result = subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Launch failed: {result.stderr}"

    # Verify container exists and is running
    result = subprocess.run(
        [coi_binary, "container", "running", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Container should be running"

    # Stop container
    result = subprocess.run(
        [coi_binary, "container", "stop", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Stop failed: {result.stderr}"

    # Verify container exists but not running
    result = subprocess.run(
        [coi_binary, "container", "exists", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Container should still exist"

    result = subprocess.run(
        [coi_binary, "container", "running", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "Container should not be running"

    # Start container again
    result = subprocess.run(
        [coi_binary, "container", "start", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Start failed: {result.stderr}"

    # Verify running
    result = subprocess.run(
        [coi_binary, "container", "running", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Container should be running after start"

    # Delete container
    result = subprocess.run(
        [coi_binary, "container", "delete", container_name, "--force"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Delete failed: {result.stderr}"

    # Verify deleted
    result = subprocess.run(
        [coi_binary, "container", "exists", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "Container should be deleted"


