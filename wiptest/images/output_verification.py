"""
Test images command produces output.

Expected:
- Command shows image listing or appropriate message
"""

import subprocess


def test_images_shows_output(coi_binary):
    """Test that images command produces output."""
    result = subprocess.run([coi_binary, "images"], capture_output=True, text=True, timeout=10)

    assert result.returncode == 0
    output = result.stdout + result.stderr

    # Should show some output (even if no images, should say so)
    assert len(output.strip()) > 0, "Images command should produce some output"
