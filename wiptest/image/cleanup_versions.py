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


def test_image_cleanup_versions(coi_binary, cleanup_containers):
    """Test cleaning up old image versions."""
    prefix = "coi-test-version-"

    # Create 5 versioned images
    for i in range(5):
        container_name = f"coi-test-ver-{i}"
        image_alias = f"{prefix}{i:02d}-20260108-{i:02d}0000"

        # Launch and publish container
        subprocess.run(
            [coi_binary, "container", "launch", "images:ubuntu/22.04", container_name],
            check=True,
        )
        time.sleep(2)

        subprocess.run(
            [coi_binary, "image", "publish", container_name, image_alias],
            check=True,
        )
        time.sleep(1)

    # Verify all 5 images exist
    result = subprocess.run(
        [coi_binary, "image", "list", "--prefix", prefix, "--format", "json"],
        capture_output=True,
        text=True,
    )
    images_before = json.loads(result.stdout)
    total_aliases_before = sum(len(img["aliases"]) for img in images_before)
    assert total_aliases_before >= 5, f"Should have at least 5 versioned images, got {total_aliases_before}"

    # Cleanup - keep only 2 most recent
    result = subprocess.run(
        [coi_binary, "image", "cleanup", prefix, "--keep", "2"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Cleanup failed: {result.stderr}"
    assert "deleted" in result.stderr.lower()

    # Verify only 2 images remain
    result = subprocess.run(
        [coi_binary, "image", "list", "--prefix", prefix, "--format", "json"],
        capture_output=True,
        text=True,
    )
    images_after = json.loads(result.stdout)
    total_aliases_after = sum(len(img["aliases"]) for img in images_after)
    assert total_aliases_after == 2, f"Should have 2 images after cleanup, got {total_aliases_after}"

    # Cleanup remaining images
    for img in images_after:
        for alias in img["aliases"]:
            subprocess.run([coi_binary, "image", "delete", alias], check=False)


