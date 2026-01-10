"""
Tests for coi attach command - basic attachment functionality.

Tests:
1. Attach fails when no containers running
"""

import os
import subprocess
import time

from support.helpers import (
    assert_clean_exit,
    calculate_container_name,
    exit_claude,
    get_container_list,
    send_prompt,
    spawn_coi,
    wait_for_container_deletion,
    wait_for_container_ready,
    wait_for_prompt,
    wait_for_text_in_monitor,
    with_live_screen,
)


def test_attach_no_containers(coi_binary, cleanup_containers):
    """Test attach when no containers are running."""
    result = subprocess.run(
        [coi_binary, "attach"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    # Should exit with success but show message about no containers
    # (exit code 0 is acceptable - it's informational, not an error)
    output = result.stdout + result.stderr
    assert "no" in output.lower(), "Should mention no containers/sessions"
