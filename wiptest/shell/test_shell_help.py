"""
Test shell subcommand with full end-to-end functionality.

Flow:
1. Launch ephemeral shell
2. Wait for Claude to be ready
3. Send a simple prompt
4. Verify Claude responds correctly
5. Exit and verify clean shutdown

Expected:
- Shell launches successfully
- Container is created
- Claude is ready and responding
- Container is cleaned up after exit
"""

import os
import time

from support.helpers import (
    assert_clean_exit,
    exit_claude,
    send_prompt,
    spawn_coi,
    wait_for_container_deletion,
    wait_for_container_ready,
    wait_for_prompt,
    wait_for_text_in_monitor,
    with_live_screen,
)


def test_shell_basic_functionality(coi_binary, cleanup_containers, workspace_dir, fake_claude_path):
    """Test that coi shell launches and works end-to-end."""
    # Use fake Claude for faster testing
    env = os.environ.copy()
    env["PATH"] = f"{fake_claude_path}:{env.get('PATH', '')}"

    # Launch ephemeral shell without tmux
    child = spawn_coi(coi_binary, ["shell", "--tmux=false"], cwd=workspace_dir, env=env)

    # Wait for container to be ready
    wait_for_container_ready(child, timeout=60)

    # Wait for Claude prompt
    wait_for_prompt(child, timeout=90)

    # Interact with Claude
    with with_live_screen(child) as monitor:
        time.sleep(2)

        # Send a simple prompt
        send_prompt(child, "Print the first 5 digits of PI")

        # Verify Claude responds with correct answer (looking for "1415" which appears in "3.1415")
        responded = wait_for_text_in_monitor(monitor, "1415", timeout=30)

        # Exit Claude and wait for container cleanup
        clean_exit = exit_claude(child)
        wait_for_container_deletion()

    # Verify test passed
    assert responded, "Claude did not respond with expected answer containing '1415' (from PI)"
    assert_clean_exit(clean_exit, child)
