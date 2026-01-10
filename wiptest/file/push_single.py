"""
Integration tests for file CLI commands.

Tests:
- coi file push (single file)
- coi file push -r (directory)
- coi file pull -r (directory)
"""

import subprocess
import time


def test_file_push_single(coi_binary, cleanup_containers, tmp_path):
    """Test pushing a single file to a container."""
    container_name = "coi-test-file-push"

    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content for push")

    # Launch container
    subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
        check=True,
    )
    time.sleep(3)

    # Push file
    result = subprocess.run(
        [coi_binary, "file", "push", str(test_file), f"{container_name}:/tmp/test.txt"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Push failed: {result.stderr}"
    assert "pushed" in result.stderr.lower()

    # Verify file exists in container
    result = subprocess.run(
        [coi_binary, "container", "exec", container_name, "--capture", "--",
         "cat", "/tmp/test.txt"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Reading pushed file failed: {result.stderr}"
    assert "test content for push" in result.stdout

    # Cleanup
    subprocess.run([coi_binary, "container", "delete", container_name, "--force"], check=False)


