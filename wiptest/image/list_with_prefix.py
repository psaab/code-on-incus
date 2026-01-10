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


def test_image_list_with_prefix(coi_binary):
    """Test listing images with prefix filter."""
    result = subprocess.run(
        [coi_binary, "image", "list", "--prefix", "coi-", "--format", "json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"List with prefix failed: {result.stderr}"

    images = json.loads(result.stdout)
    # All aliases should start with coi-
    for img in images:
        for alias in img["aliases"]:
            assert alias.startswith("coi-"), f"Alias {alias} should start with coi-"


