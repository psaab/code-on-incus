"""
Test images command help functionality.

Expected:
- Help flag works and shows usage
"""

import subprocess


def test_images_help_flag(coi_binary):
    """Test that coi images --help shows help."""
    result = subprocess.run(
        [coi_binary, "images", "--help"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    assert "images" in result.stdout.lower()
    assert "usage:" in result.stdout.lower() or "list" in result.stdout.lower()
