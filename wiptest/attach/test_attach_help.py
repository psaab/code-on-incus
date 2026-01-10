"""
Test attach subcommand with full end-to-end functionality.

Flow:
1. Launch persistent shell with tmux on slot 1
2. Interact with Claude to verify it works
3. Detach from tmux (keeps container running)
4. Attach from a new process to the running container
5. Verify we can interact with Claude in the attached session
6. Exit cleanly

Expected:
- Can launch persistent shell with tmux
- Can detach using tmux sequence without stopping container
- Can attach to running persistent container
- Can interact with Claude through attached session
- Container is cleaned up after final exit
"""

import os
import subprocess
import time

from pexpect import EOF

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


def test_attach_to_running_container(
    coi_binary, cleanup_containers, workspace_dir, fake_claude_path
):
    """Test that coi attach works to reconnect to a running persistent container."""
    # Use fake Claude for faster testing
    env = os.environ.copy()
    env["PATH"] = f"{fake_claude_path}:{env.get('PATH', '')}"

    # Launch persistent shell WITH tmux (default behavior)
    child1 = spawn_coi(
        coi_binary,
        ["shell", "--persistent", "--slot=1"],  # tmux is enabled by default
        cwd=workspace_dir,
        env=env
    )

    # Wait for container and Claude to be ready
    wait_for_container_ready(child1, timeout=60)
    wait_for_prompt(child1, timeout=90)

    # Verify container is running
    container_name = calculate_container_name(workspace_dir, 1)
    containers = get_container_list()
    assert container_name in containers, f"Container {container_name} should be running"

    # Interact with Claude to verify it's working before detach
    with with_live_screen(child1) as monitor:
        time.sleep(2)
        send_prompt(child1, "What is 2+2?")
        responded = wait_for_text_in_monitor(monitor, "4", timeout=30)
        assert responded, "Claude should respond before detach"

    # Detach from tmux session (Ctrl+B, d) - this keeps container running
    child1.sendcontrol('b')
    time.sleep(0.5)
    child1.send('d')
    time.sleep(2)

    # Wait for child1 to exit (detach causes the coi process to exit, but container stays)
    try:
        child1.expect(EOF, timeout=10)
        child1.close()
    except Exception:
        # Force close if needed
        child1.close(force=True)

    # Give container a moment to stabilize
    time.sleep(2)

    # Verify container is STILL running after detach
    containers = get_container_list()
    assert container_name in containers, \
        f"Container {container_name} should still be running after tmux detach"

    # Now attach to the running container from a new process
    child2 = spawn_coi(
        coi_binary,
        ["attach", "--slot=1"],
        cwd=workspace_dir,
        env=env
    )

    # Should reconnect to the existing Claude session
    # This should be faster since container is already running
    wait_for_prompt(child2, timeout=30)

    # Interact with Claude again through the attached session
    with with_live_screen(child2) as monitor:
        time.sleep(2)
        send_prompt(child2, "What is 3+3?")
        responded = wait_for_text_in_monitor(monitor, "6", timeout=30)
        assert responded, "Claude should respond after attach"

        # Exit cleanly this time (will stop and clean up the container)
        clean_exit = exit_claude(child2)
        wait_for_container_deletion()

    # Verify clean exit
    assert_clean_exit(clean_exit, child2)
