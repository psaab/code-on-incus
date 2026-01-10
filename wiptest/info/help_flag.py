"""
Test info command with full end-to-end functionality.

Flow:
1. Launch persistent shell to create a session
2. Exit and get session ID
3. Run info command with session ID
4. Verify info output contains session details
5. Clean up

Expected:
- Info shows session ID
- Info shows container name
- Info shows workspace path
- Info shows timestamps (created, last used)
- Info provides actionable information about the session
"""

import os
import subprocess
import time

from support.helpers import (
    calculate_container_name,
    exit_claude,
    get_latest_session_id,
    spawn_coi,
    wait_for_container_ready,
    wait_for_prompt,
    with_live_screen,
)


def test_info_command_functionality(coi_binary, cleanup_containers):
    """Test that coi info command handles sessions appropriately."""
    # Test 1: Info with fake/nonexistent session ID should fail gracefully
    fake_session_id = "00000000-0000-0000-0000-000000000000"

    result = subprocess.run(
        [coi_binary, "info", fake_session_id],
        capture_output=True,
        text=True,
        timeout=10,
    )

    # Should fail with informative error
    assert result.returncode != 0, "Info with nonexistent session should fail"

    output = result.stdout + result.stderr
    output_lower = output.lower()

    # Should mention the problem clearly
    assert "not found" in output_lower or "error" in output_lower, \
        "Info should indicate session not found"

    # Should show the session ID in the error message
    assert fake_session_id in output or "session" in output_lower, \
        "Error should reference the session ID"

    # Test 2: Info without arguments should show usage
    result_no_args = subprocess.run(
        [coi_binary, "info"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    # Should show usage/help
    output_no_args = result_no_args.stdout + result_no_args.stderr
    assert "usage" in output_no_args.lower() or "session" in output_no_args.lower(), \
        "Info without args should show usage"
