"""
Integration tests for file CLI commands.

Tests:
- coi file push (single file)
- coi file push -r (directory)
- coi file pull -r (directory)
"""

import subprocess
import time


def test_file_pull_directory(coi_binary, cleanup_containers, tmp_path):
    """Test pulling a directory from a container."""
    container_name = "coi-test-file-pull"

    # Launch container
    subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
        check=True,
    )
    time.sleep(3)

    # Create test files in container
    subprocess.run(
        [coi_binary, "container", "exec", container_name, "--",
         "mkdir", "-p", "/tmp/pull_test/subdir"],
        check=True,
    )
    subprocess.run(
        [coi_binary, "container", "exec", container_name, "--",
         "sh", "-c", "echo 'pulled content 1' > /tmp/pull_test/file1.txt"],
        check=True,
    )
    subprocess.run(
        [coi_binary, "container", "exec", container_name, "--",
         "sh", "-c", "echo 'pulled content 2' > /tmp/pull_test/subdir/file2.txt"],
        check=True,
    )

    # Pull directory
    pull_dest = tmp_path / "pulled"
    result = subprocess.run(
        [coi_binary, "file", "pull", "-r", f"{container_name}:/tmp/pull_test", str(pull_dest)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Pull failed: {result.stderr}"

    # Verify files were pulled
    file1 = pull_dest / "file1.txt"
    assert file1.exists(), "file1.txt should be pulled"
    assert "pulled content 1" in file1.read_text()

    file2 = pull_dest / "subdir" / "file2.txt"
    assert file2.exists(), "subdir/file2.txt should be pulled"
    assert "pulled content 2" in file2.read_text()

    # Cleanup
    subprocess.run([coi_binary, "container", "delete", container_name, "--force"], check=False)


