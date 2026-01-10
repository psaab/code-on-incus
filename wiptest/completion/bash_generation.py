"""
Test completion bash script generation.

Expected:
- Bash completion generates valid script
"""

import subprocess


def test_completion_bash_generates_script(coi_binary):
    """Test that completion bash generates a script."""
    result = subprocess.run(
        [coi_binary, "completion", "bash"], capture_output=True, text=True, timeout=5
    )

    assert result.returncode == 0
    output = result.stdout

    # Should generate bash completion script
    assert len(output) > 100, "Should generate substantial completion script"
    # Bash completions typically have specific patterns
    assert "bash" in output.lower() or "complete" in output.lower() or "#" in output, (
        "Should look like a bash completion script"
    )
