"""
Tests for coi attach command - basic attachment functionality.

Tests:
1. Attach fails when no containers running
2. Attach to specific slot works end-to-end
"""

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


def test_attach_to_specific_slot(coi_binary, cleanup_containers, workspace_dir):
    """Test that attach --slot works to connect to a specific container slot."""
    # Use test-claude (fake Claude installed in base image) for faster tests
    env = {"COI_USE_TEST_CLAUDE": "1"}

    # Launch container on slot 1 with tmux
    child1 = spawn_coi(
        coi_binary,
        ["shell", "--persistent", "--slot=1"],
        cwd=workspace_dir,
        env=env,
    )

    wait_for_container_ready(child1, timeout=60)
    wait_for_prompt(child1, timeout=90)

    # Interact to verify it works (fake claude echoes input with -BACK suffix)
    with with_live_screen(child1) as monitor:
        time.sleep(2)
        send_prompt(child1, "slot1init")
        responded = wait_for_text_in_monitor(monitor, "slot1init-BACK", timeout=30)
        assert responded, "Slot 1 container should respond"

    # Detach from slot 1 (keeps container running)
    child1.sendcontrol('b')
    time.sleep(0.5)
    child1.send('d')
    time.sleep(2)

    try:
        child1.expect(EOF, timeout=10)
        child1.close()
    except Exception:
        child1.close(force=True)

    time.sleep(2)

    # Launch container on slot 2 with tmux
    child2 = spawn_coi(
        coi_binary,
        ["shell", "--persistent", "--slot=2"],
        cwd=workspace_dir,
        env=env,
    )

    wait_for_container_ready(child2, timeout=60)
    wait_for_prompt(child2, timeout=90)

    # Interact to verify it works
    with with_live_screen(child2) as monitor:
        time.sleep(2)
        send_prompt(child2, "slot2init")
        responded = wait_for_text_in_monitor(monitor, "slot2init-BACK", timeout=30)
        assert responded, "Slot 2 container should respond"

    # Detach from slot 2
    child2.sendcontrol('b')
    time.sleep(0.5)
    child2.send('d')
    time.sleep(2)

    try:
        child2.expect(EOF, timeout=10)
        child2.close()
    except Exception:
        child2.close(force=True)

    time.sleep(2)

    # Verify both containers are running
    container1 = calculate_container_name(workspace_dir, 1)
    container2 = calculate_container_name(workspace_dir, 2)
    containers = get_container_list()
    assert container1 in containers, f"Container {container1} (slot 1) should be running"
    assert container2 in containers, f"Container {container2} (slot 2) should be running"

    # Now attach to slot 1 specifically (not slot 2)
    child_attach1 = spawn_coi(
        coi_binary,
        ["attach", "--slot=1"],
        cwd=workspace_dir,
        env=env,
    )

    wait_for_prompt(child_attach1, timeout=30)

    # Interact to verify we're connected to slot 1
    with with_live_screen(child_attach1) as monitor:
        time.sleep(2)
        send_prompt(child_attach1, "slot1attach")
        responded = wait_for_text_in_monitor(monitor, "slot1attach-BACK", timeout=30)
        assert responded, "Should be able to interact with slot 1 after attach"

        # Detach from slot 1 (persistent containers stay running)
        child_attach1.sendcontrol('b')
        time.sleep(0.5)
        child_attach1.send('d')

    try:
        child_attach1.expect(EOF, timeout=10)
        clean_exit1 = True
        child_attach1.close()
    except Exception:
        clean_exit1 = False
        child_attach1.close(force=True)

    # Now attach to slot 2 specifically
    child_attach2 = spawn_coi(
        coi_binary,
        ["attach", "--slot=2"],
        cwd=workspace_dir,
        env=env,
    )

    wait_for_prompt(child_attach2, timeout=30)

    # Interact to verify we're connected to slot 2
    with with_live_screen(child_attach2) as monitor:
        time.sleep(2)
        send_prompt(child_attach2, "slot2attach")
        responded = wait_for_text_in_monitor(monitor, "slot2attach-BACK", timeout=30)
        assert responded, "Should be able to interact with slot 2 after attach"

        # Detach from slot 2 (persistent containers stay running)
        child_attach2.sendcontrol('b')
        time.sleep(0.5)
        child_attach2.send('d')

    try:
        child_attach2.expect(EOF, timeout=10)
        child_attach2.close()
    except Exception:
        child_attach2.close(force=True)

    # Verify both coi processes exited cleanly
    assert_clean_exit(clean_exit1, child_attach1)

    # Kill persistent containers (cleanup_containers fixture will also clean up)
    import subprocess
    subprocess.run(
        ["sg", "incus-admin", "-c", f"incus delete --force {container1}"],
        capture_output=True,
    )
    subprocess.run(
        ["sg", "incus-admin", "-c", f"incus delete --force {container2}"],
        capture_output=True,
    )
