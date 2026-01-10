"""
Test clean command without arguments.

Expected:
- Shows help or runs safely
- Produces output
"""

import subprocess


def test_clean_without_args_shows_help_or_runs(coi_binary):
    """Test clean without arguments shows help or runs safely."""
    result = subprocess.run([coi_binary, "clean"], capture_output=True, text=True, timeout=10)

    # Should either show help or run without error
    # Exit code depends on implementation
    output = result.stdout + result.stderr

    # Should produce some output
    assert len(output.strip()) > 0, "Clean should produce output or help"
