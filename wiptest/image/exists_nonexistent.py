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


def test_image_exists_nonexistent(coi_binary):
    """Test checking if a nonexistent image exists."""
    result = subprocess.run(
        [coi_binary, "image", "exists", "nonexistent-image-12345"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "Nonexistent image should return non-zero exit code"
