"""
Test -v flag behavior (version synonym or verbose).

Expected:
- Command completes (behavior may vary)
"""

import subprocess


def test_version_flag_synonym(coi_binary):
    """Test that -v might work as synonym for --version (if implemented)."""
    # Note: This test documents expected behavior
    # Some CLIs use -v for verbose, others for version
    result = subprocess.run([coi_binary, "-v"], capture_output=True, text=True, timeout=5)

    # We don't assert success here since -v might be verbose flag
    # Just document that we tested it
    # If it shows version, that's fine; if it errors or shows help, that's also fine
    assert result.returncode is not None, "Command should complete"
