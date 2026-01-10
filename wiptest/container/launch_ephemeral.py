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


def test_container_launch_ephemeral(coi_binary, cleanup_containers):
    """Test launching an ephemeral container."""
    container_name = "coi-test-launch-ephemeral"

    # Launch ephemeral container
    result = subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name, "--ephemeral"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Launch failed: {result.stderr}"
    assert "launched" in result.stderr.lower()

    # Verify container exists
    result = subprocess.run(
        [coi_binary, "container", "exists", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Container should exist"

    # Stop container (ephemeral will auto-delete)
    subprocess.run([coi_binary, "container", "stop", container_name, "--force"], check=False)
    time.sleep(2)

    # Verify container no longer exists (ephemeral)
    result = subprocess.run(
        [coi_binary, "container", "exists", container_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "Ephemeral container should be deleted"


