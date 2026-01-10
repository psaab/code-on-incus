"""
Integration tests for file CLI commands.

Tests:
- coi file push (single file)
- coi file push -r (directory)
- coi file pull -r (directory)
"""

import subprocess
import time


def test_file_push_without_recursive_flag(coi_binary, cleanup_containers, tmp_path):
    """Test that pushing a directory without -r flag fails."""
    container_name = "coi-test-file-push-no-r"

    # Create test directory
    test_dir = tmp_path / "test_dir_no_r"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("content")

    # Launch container
    subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
        check=True,
    )
    time.sleep(3)

    # Try to push directory without -r (should fail)
    result = subprocess.run(
        [coi_binary, "file", "push", str(test_dir), f"{container_name}:/tmp/test_dir"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "Push directory without -r should fail"
    assert "use -r flag" in result.stderr.lower() or "directory" in result.stderr.lower()

    # Cleanup
    subprocess.run([coi_binary, "container", "delete", container_name, "--force"], check=False)
