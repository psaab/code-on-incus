"""
Test that ephemeral mode does not persist files, even when using --resume.

Flow:
1. Start first ephemeral session (without --persistent)
2. Create test file in ~/
3. Exit session (container should be deleted)
4. Resume session with --resume
5. Verify test file does NOT exist (new container, no persistence)
6. Exit session

Expected:
- First container is deleted after exit (ephemeral mode)
- Resume creates a NEW container (not reusing old one)
- Files from first session do NOT persist to resumed session
- This ensures ephemeral mode is truly ephemeral
"""

import time
import os

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


def test_ephemeral_no_persistence_on_resume(coi_binary, cleanup_containers, workspace_dir, fake_claude_path):
    """Test that ephemeral mode does not persist files, even when resuming."""

    # First session WITHOUT --persistent (ephemeral mode)
    # Use fake Claude for faster testing (10x+ speedup)

    env = os.environ.copy()

    env["PATH"] = f"{fake_claude_path}:{env.get('PATH', '')}"


    child = spawn_coi(coi_binary, ["shell", "--tmux=true"], cwd=workspace_dir, env=env)

    wait_for_container_ready(child)

    # Get container name from first session
    import subprocess
    result1 = subprocess.run(
        ["sg", "incus-admin", "-c", "incus list --format=csv -c n"],
        capture_output=True,
        text=True,
        shell=False,
    )
    containers_before = set(result1.stdout.strip().split('\n')) if result1.stdout.strip() else set()
    print(f"\n\nContainers before first session: {containers_before}")

    wait_for_prompt(child)

    with with_live_screen(child) as monitor:
        time.sleep(2)

        # Create test file in home directory
        send_prompt(child, "mkdir -p ~/ephemeral_test && echo 'should-not-persist' > ~/ephemeral_test/data.txt")
        send_prompt(child, "Print ONLY result of sum of 3000 and 4000 and NOTHING ELSE")
        file_created = wait_for_text_in_monitor(monitor, "7000", timeout=30)
        assert file_created, "Failed to create test file in first session"

        # Exit first session (container should be deleted)
        time.sleep(1)
        clean_exit = exit_claude(child, timeout=90)
        wait_for_container_deletion()

    assert_clean_exit(clean_exit, child)

    # Give a moment for container to be deleted
    time.sleep(3)

    # Check containers after deletion
    result2 = subprocess.run(
        ["sg", "incus-admin", "-c", "incus list --format=csv -c n"],
        capture_output=True,
        text=True,
        shell=False,
    )
    containers_after_delete = set(result2.stdout.strip().split('\n')) if result2.stdout.strip() else set()
    print(f"Containers after deletion: {containers_after_delete}")
    print(f"Container was deleted: {containers_before == containers_after_delete}")

    # Second session with --resume (should create new container, not reuse)
    child2 = spawn_coi(coi_binary, ["shell", "--tmux=true", "--resume"], cwd=workspace_dir)

    wait_for_container_ready(child2)

    # Check which container is being used
    result3 = subprocess.run(
        ["sg", "incus-admin", "-c", "incus list --format=csv -c n"],
        capture_output=True,
        text=True,
        shell=False,
    )
    containers_second_session = set(result3.stdout.strip().split('\n')) if result3.stdout.strip() else set()
    print(f"Containers in second session: {containers_second_session}")
    new_containers = containers_second_session - containers_before
    print(f"New containers created: {new_containers}")
    # Give extra time for Claude to load from restored session
    time.sleep(5)
    wait_for_prompt(child2)

    with with_live_screen(child2) as monitor2:
        time.sleep(2)

        # Try to check if file exists - it should NOT (different approach from filesystem_persistence)
        # Ask Claude to check and print a unique number if file exists
        send_prompt(
            child2,
            "CHECK IF ~/ephemeral_test/data.txt exists and print ONLY result of 5000+6000 if YES AND NOTHING ELSE",
        )

        # If file exists, Claude will print 11000
        # If file doesn't exist, Claude should not print that number
        # Wait a bit to see what appears
        time.sleep(5)
        screen_text = monitor2.get_current_screen()
        file_found = "11000" in screen_text

        # Debug: print what we see
        print(f"\n\n=== DEBUG OUTPUT ===")
        print(f"file_found (11000 seen): {file_found}")
        print(f"\nScreen text (get_current_screen):\n{screen_text}")
        print(f"\nFull monitor.last_display:\n{monitor2.last_display}")
        print(f"===================\n")

        # Exit second session
        time.sleep(1)
        clean_exit2 = exit_claude(child2, timeout=90)
        wait_for_container_deletion()

    # Verify that file did NOT persist
    assert not file_found, (
        "File from first ephemeral session incorrectly persisted to resumed session"
    )
    assert_clean_exit(clean_exit2, child2)
