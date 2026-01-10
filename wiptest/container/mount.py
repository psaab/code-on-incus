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


def test_container_mount(coi_binary, cleanup_containers, tmp_path):
    """Test mounting a directory to a container."""
    container_name = "coi-test-mount"

    # Create test directory
    test_dir = tmp_path / "mount_test"
    test_dir.mkdir()
    (test_dir / "test.txt").write_text("mount test content")

    # Launch container
    subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
        check=True,
    )
    time.sleep(3)

    # Mount directory
    result = subprocess.run(
        [coi_binary, "container", "mount", container_name, "testmount",
         str(test_dir), "/mnt/test", "--shift"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Mount failed: {result.stderr}"

    # Verify mount worked by reading file
    time.sleep(2)
    result = subprocess.run(
        [coi_binary, "container", "exec", container_name, "--capture", "--",
         "cat", "/mnt/test/test.txt"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Reading mounted file failed: {result.stderr}"
    assert "mount test content" in result.stdout

    # Cleanup
    subprocess.run([coi_binary, "container", "delete", container_name, "--force"], check=False)
