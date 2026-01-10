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


def test_image_list_json(coi_binary):
    """Test listing images in JSON format."""
    result = subprocess.run(
        [coi_binary, "image", "list", "--format", "json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"List failed: {result.stderr}"

    # Verify JSON output
    images = json.loads(result.stdout)
    assert isinstance(images, list), "Output should be a JSON array"


