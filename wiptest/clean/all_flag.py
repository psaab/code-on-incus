"""
Test that clean --all flag works.

Expected:
- All flag is recognized
- Help works with --all flag
"""

import subprocess


def test_clean_all_flag(coi_binary):
    """Test that clean --all flag works."""
    # Note: This is dangerous, so we use it carefully
    # It should work but we verify it doesn't crash
    result = subprocess.run(
        [coi_binary, "clean", "--all", "--help"],  # Use --help to not actually clean
        capture_output=True,
        text=True,
        timeout=5,
    )

    # Help should work even with --all flag
    assert result.returncode == 0
    assert "all" in result.stdout.lower()
