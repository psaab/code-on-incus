"""
Test images command mentions coi-related images.

Expected:
- Output mentions coi images or shows no images message
"""

import subprocess


def test_images_mentions_coi_images(coi_binary):
    """Test that images output mentions coi-related images."""
    result = subprocess.run([coi_binary, "images"], capture_output=True, text=True, timeout=10)

    assert result.returncode == 0
    output = (result.stdout + result.stderr).lower()

    # Should mention coi images or show no images message
    assert "coi" in output or "image" in output or "no" in output or "available" in output, (
        "Should mention images or show appropriate message"
    )
