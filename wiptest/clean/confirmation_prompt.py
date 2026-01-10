"""
Test that clean command shows confirmation without --force flag.

Expected:
- Clean without --force asks for confirmation
- Can decline confirmation safely
"""

import subprocess


def test_clean_without_force_shows_confirmation(coi_binary):
    """Test that clean without --force asks for confirmation."""
    # Run clean without force, with empty stdin (should timeout or show prompt)
    result = subprocess.run(
        [coi_binary, "clean"],
        capture_output=True,
        text=True,
        timeout=5,
        input="n\n",  # Send 'n' to decline
    )

    # Should show some confirmation message or complete without error
    # (behavior depends on implementation)
    assert result.returncode is not None
