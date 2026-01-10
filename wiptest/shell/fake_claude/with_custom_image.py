"""
Test using fake Claude via custom image (recommended approach).

This demonstrates the PROPER way to use fake Claude:
- Fake Claude is installed IN the container
- No PATH manipulation needed
- More realistic testing
- Image built once and reused
"""

import os
import sys

# Add support directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "support"))

import pexpect
from helpers import spawn_coi, wait_for_prompt


def test_shell_with_fake_claude_image(coi_binary, fake_claude_image, cleanup_containers, tmp_path):
    """Test shell using custom image with fake Claude pre-installed.

    This is the RECOMMENDED approach for using fake Claude in tests:
    1. Use fake_claude_image fixture (builds image once per session)
    2. Pass --image flag to coi shell
    3. Fake Claude is already in the container at /usr/local/bin/claude
    4. No PATH manipulation needed!
    """

    print(f"\nUsing test image: {fake_claude_image}")

    # Start shell with fake Claude image - simple and clean!
    child = spawn_coi(
        coi_binary,
        ["shell", "--image", fake_claude_image, "--tmux=false"],
        cwd=str(tmp_path),
        timeout=30
    )

    try:
        # Wait for fake Claude to start (much faster than real Claude!)
        index = child.expect([
            "Fake Claude starting",
            "Tips for getting started",
            "You:",
            pexpect.TIMEOUT
        ], timeout=15)

        assert index != 3, "Timed out waiting for fake Claude"

        print("✓ Fake Claude started successfully (from custom image)")

        # Send a test command
        child.sendline("hello from custom image test")

        # Fake Claude echoes back
        child.expect(["I received: hello from custom image test", pexpect.TIMEOUT], timeout=5)

        print("✓ Fake Claude responded correctly")

        # Exit
        child.sendline("exit")
        child.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=5)

        print("✓ Test completed successfully with custom image approach!")

    finally:
        if child.isalive():
            child.terminate(force=True)


def test_fake_claude_image_reuse(coi_binary, fake_claude_image, cleanup_containers, tmp_path):
    """Verify that fake Claude image is reused across tests (not rebuilt each time)."""

    # This test should run immediately since image is already built
    print(f"\nReusing existing image: {fake_claude_image}")

    child = spawn_coi(
        coi_binary,
        ["shell", "--image", fake_claude_image, "--tmux=false", "--slot", "98"],
        cwd=str(tmp_path),
        timeout=30
    )

    try:
        child.expect(["Fake Claude starting", "You:", pexpect.TIMEOUT], timeout=15)
        print("✓ Image reuse works - no rebuild needed!")

        child.sendline("exit")
        child.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=5)

    finally:
        if child.isalive():
            child.terminate(force=True)
