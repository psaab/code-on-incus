"""
Test that --mount-claude-config=false works in persistent mode.

Flow:
1. Start persistent session with --mount-claude-config=false
2. Verify initial Claude setup prompts appear (no pre-configured environment)
3. Exit

Expected:
- Initial Claude setup appears even in persistent mode when config not mounted
- Container is created and persists
"""

import subprocess
import time

from support.helpers import (
    assert_clean_exit,
    calculate_container_name,
    exit_claude,
    spawn_coi,
    wait_for_container_ready,
    wait_for_text_in_monitor,
    with_live_screen,
)


def test_persistent_no_mount_shows_initial_setup(coi_binary, cleanup_containers, workspace_dir):
    """Test that --mount-claude-config=false shows initial Claude setup in persistent mode."""

    # Start persistent session with --mount-claude-config=false
    child = spawn_coi(
        coi_binary,
        ["shell", "--tmux=true", "--persistent", "--slot=26", "--mount-claude-config=false"],
        cwd=workspace_dir,
    )

    wait_for_container_ready(child)
    container_name = calculate_container_name(workspace_dir, 26)

    with with_live_screen(child) as monitor:
        # Wait for initial setup to appear
        time.sleep(10)

        # Check for initial Claude setup prompts
        setup_found = (
            wait_for_text_in_monitor(monitor, "Light mode", timeout=30)
            or wait_for_text_in_monitor(monitor, "Dark mode", timeout=5)
        )

        if not setup_found:
            # Debug: print what we actually see
            print(f"\nScreen content:\n{monitor.last_display}\n")

        assert setup_found, (
            "Expected initial Claude setup prompts to appear in persistent mode "
            "with --mount-claude-config=false, but they were not found"
        )

        # Exit Claude - use Ctrl+C since we're in setup, not at prompt
        time.sleep(1)
        clean_exit = exit_claude(child, use_ctrl_c=True, timeout=30)

    assert_clean_exit(clean_exit, child)

    # Verify container exists and is stopped (persistent mode)
    time.sleep(2)
    result = subprocess.run(
        ["sg", "incus-admin", "-c", f"incus list {container_name} --format=csv"],
        capture_output=True,
        text=True,
        shell=False,
    )
    assert container_name in result.stdout, f"Container {container_name} should exist (persistent mode)"
    assert "STOPPED" in result.stdout, "Container should be stopped"

    # Cleanup
    subprocess.run(
        ["sg", "incus-admin", "-c", f"incus delete --force {container_name}"],
        check=False,
        shell=False,
    )
