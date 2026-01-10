"""
Integration tests for image CLI commands.

Tests:
- coi image list
- coi image publish
- coi image delete
- coi image exists
- coi image cleanup (version management)
"""

import json
import subprocess
import time


def test_image_publish_and_delete(coi_binary, cleanup_containers):
    """Test publishing a container as an image and deleting it."""
    container_name = "coi-test-publish"
    image_alias = "coi-test-image"

    # Launch container
    subprocess.run(
        [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
        check=True,
    )
    time.sleep(3)

    # Make a small change to the container
    subprocess.run(
        [coi_binary, "container", "exec", container_name, "--",
         "sh", "-c", "echo 'test' > /test.txt"],
        check=True,
    )

    # Publish container
    result = subprocess.run(
        [coi_binary, "image", "publish", container_name, image_alias,
         "--description", "Test image"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Publish failed: {result.stderr}"

    # Verify JSON output
    output = json.loads(result.stdout)
    assert "fingerprint" in output
    assert output["alias"] == image_alias

    # Verify image exists
    result = subprocess.run(
        [coi_binary, "image", "exists", image_alias],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Image should exist after publish"

    # Delete image
    result = subprocess.run(
        [coi_binary, "image", "delete", image_alias],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Delete failed: {result.stderr}"

    # Verify image no longer exists
    result = subprocess.run(
        [coi_binary, "image", "exists", image_alias],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "Image should not exist after delete"


