"""
Integration tests for file CLI commands.

Tests:
- coi file push (single file)
- coi file push -r (directory)
- coi file pull -r (directory)
"""

import subprocess
import time


def test_file_push_directory(coi_binary, cleanup_containers, tmp_path):
    """Test pushing a directory to a container."""
    container_name = "coi-test-file-push-dir"

    # Create test directory structure
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file1.txt").write_text("content 1")
    (test_dir / "file2.txt").write_text("content 2")
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "file3.txt").write_text("content 3")

    # Launch container
    subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
        check=True,
    )
    time.sleep(3)

    # Push directory
    result = subprocess.run(
        [coi_binary, "file", "push", "-r", str(test_dir), f"{container_name}:/tmp/test_dir"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Push directory failed: {result.stderr}"

    # Verify files exist in container
    result = subprocess.run(
        [coi_binary, "container", "exec", container_name, "--capture", "--",
         "cat", "/tmp/test_dir/file1.txt"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "file1.txt should exist"
    assert "content 1" in result.stdout

    result = subprocess.run(
        [coi_binary, "container", "exec", container_name, "--capture", "--",
         "cat", "/tmp/test_dir/subdir/file3.txt"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "subdir/file3.txt should exist"
    assert "content 3" in result.stdout

    # Cleanup
    subprocess.run([coi_binary, "container", "delete", container_name, "--force"], check=False)


