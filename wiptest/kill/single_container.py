"""
Tests for coi kill command - killing single containers.
"""

import subprocess
import time

def test_kill_running_container(coi_binary, cleanup_containers):
    """Test killing a running container."""
    # Launch a container first
    result = subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", "coi-test-kill-1"],
        check=True,
        capture_output=True,
    )
    time.sleep(3)
    
    # Verify it's running
    result = subprocess.run(
        [coi_binary, "container", "running", "coi-test-kill-1"],
        capture_output=True,
    )
    assert result.returncode == 0, "Container should be running"
    
    # Kill it
    result = subprocess.run(
        [coi_binary, "kill", "coi-test-kill-1", "--force"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Kill failed: {result.stderr}"
    time.sleep(2)
    
    # Verify it no longer exists
    result = subprocess.run(
        [coi_binary, "container", "exists", "coi-test-kill-1"],
        capture_output=True,
    )
    assert result.returncode != 0, "Container should not exist after kill"


def test_kill_nonexistent_container(coi_binary):
    """Test killing a container that doesn't exist."""
    result = subprocess.run(
        [coi_binary, "kill", "nonexistent-container-12345", "--force"],
        capture_output=True,
        text=True,
    )
    # Should fail gracefully
    assert result.returncode != 0, "Should fail when container doesn't exist"
