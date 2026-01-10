"""
Test completion help mentions supported shells.

Expected:
- Help shows available shells (bash, zsh, fish, powershell)
"""

import subprocess


def test_completion_help_shows_shells(coi_binary):
    """Test that completion help mentions supported shells."""
    result = subprocess.run(
        [coi_binary, "completion", "--help"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    output = result.stdout.lower()

    # Should mention shell types
    shells = ["bash", "zsh", "fish", "powershell"]
    found_shells = [shell for shell in shells if shell in output]

    assert len(found_shells) >= 2, f"Should mention common shells, found: {found_shells}"
