"""
Test completion fish script generation.

Expected:
- Fish completion generates valid script
"""

import subprocess


def test_completion_fish_generates_script(coi_binary):
    """Test that completion fish generates a script."""
    result = subprocess.run(
        [coi_binary, "completion", "fish"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    output = result.stdout

    # Should generate fish completion script
    assert len(output) > 50, "Should generate substantial completion script"
