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


def test_container_exec(coi_binary, cleanup_containers):
    """Test executing commands in a container."""
    container_name = "coi-test-exec"

    # Launch container
    subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
        check=True,
    )
    time.sleep(3)  # Wait for container to be ready

    # Execute simple command
    result = subprocess.run(
        [coi_binary, "container", "exec", container_name, "--", "echo", "hello"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Exec failed: {result.stderr}"
    assert "hello" in result.stderr or "hello" in result.stdout

    # Execute with capture (JSON output)
    result = subprocess.run(
        [coi_binary, "container", "exec", container_name, "--capture", "--", "echo", "test123"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Exec with capture failed: {result.stderr}"
    assert "test123" in result.stdout
    assert "stdout" in result.stdout  # JSON format

    # Cleanup
    subprocess.run([coi_binary, "container", "delete", container_name, "--force"], check=False)


