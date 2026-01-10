"""
Test images command with full output format validation.

Expected:
- Command runs without errors
- Output shows COI images section
- Output shows coi image status (built or not built)
- Output shows remote images section
- Output format is properly structured
"""

import subprocess


def test_images_command_basic(coi_binary):
    """Test that coi images runs and shows proper output format."""
    result = subprocess.run(
        [coi_binary, "images"], capture_output=True, text=True, timeout=10
    )

    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"

    output = result.stdout + result.stderr
    output_lower = output.lower()

    # Verify output has substantial content
    assert len(output.strip()) > 100, "Images output should be informative (> 100 chars)"

    # Should mention "COI images" or "available images"
    assert "coi" in output_lower or "image" in output_lower, \
        "Output should mention images"

    # Should list the core COI image
    assert "coi" in output, \
        "Output should mention coi image"

    # Should indicate build status (built, not built, or checkmarks)
    has_status_indicator = any(indicator in output_lower for indicator in [
        "built", "not built", "build with:", "✓", "✗", "available"
    ])
    assert has_status_indicator, \
        "Output should indicate whether images are built or not"

    # Should mention remote images section
    assert "remote" in output_lower or "ubuntu" in output_lower or "debian" in output_lower, \
        "Output should mention remote images availability"

    # Should provide useful information (not just a list)
    # Look for descriptions or helpful text
    assert ":" in output or "-" in output or "•" in output, \
        "Output should be structured (colons, dashes, or bullets)"

    # Verify output is multi-line (not a single line dump)
    lines = output.strip().split('\n')
    assert len(lines) >= 5, "Output should be multi-line with multiple sections"
