"""
Test completion zsh script generation.

Expected:
- Zsh completion generates valid script
"""

import subprocess


def test_completion_zsh_generates_script(coi_binary):
    """Test that completion zsh generates a script."""
    result = subprocess.run(
        [coi_binary, "completion", "zsh"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    output = result.stdout

    # Should generate zsh completion script
    assert len(output) > 100, "Should generate substantial completion script"
    # Zsh completions typically have specific patterns
    assert "zsh" in output.lower() or "compdef" in output.lower() or "#" in output, (
        "Should look like a zsh completion script"
    )
