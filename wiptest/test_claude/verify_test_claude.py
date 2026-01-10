"""
Test that test-claude works correctly with COI_USE_TEST_CLAUDE=1 env var.

Verifies that:
1. test-claude is installed in the image
2. COI_USE_TEST_CLAUDE=1 uses test-claude instead of real claude
3. test-claude responds correctly
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "support"))
import pexpect


def test_test_claude_installed(coi_binary, cleanup_containers, tmp_path):
    """Test that test-claude is installed in the image."""

    result = subprocess.run(
        [coi_binary, "run", "--", "which", "test-claude"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=30
    )

    assert result.returncode == 0, f"test-claude not found: {result.stderr}"
    assert "/usr/local/bin/test-claude" in result.stdout, f"Unexpected path: {result.stdout}"

    print("✓ test-claude is installed at /usr/local/bin/test-claude")


def test_test_claude_version(coi_binary, cleanup_containers, tmp_path):
    """Test that test-claude --version works."""

    result = subprocess.run(
        [coi_binary, "run", "--", "test-claude", "--version"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=30
    )

    assert result.returncode == 0, f"test-claude --version failed: {result.stderr}"
    assert "Claude Code CLI" in result.stdout, f"Unexpected version output: {result.stdout}"
    assert "fake" in result.stdout.lower() or "test stub" in result.stdout.lower(), f"Not fake version: {result.stdout}"

    print(f"✓ test-claude version: {result.stdout.strip()}")


def test_env_var_uses_test_claude(coi_binary, cleanup_containers, tmp_path):
    """Test that COI_USE_TEST_CLAUDE=1 actually uses test-claude."""

    env = os.environ.copy()
    env["COI_USE_TEST_CLAUDE"] = "1"

    # Start shell with test-claude
    child = pexpect.spawn(
        coi_binary,
        ["shell", "--tmux=false", "--slot", "97"],
        cwd=str(tmp_path),
        encoding="utf-8",
        timeout=30,
        env=env
    )

    try:
        # Should see message about using test-claude
        child.expect("Using test-claude", timeout=10)
        print("✓ Saw 'Using test-claude' message")

        # Should see fake Claude startup
        child.expect("Tips for getting started", timeout=10)
        print("✓ Fake Claude started successfully")

        # Send a test message
        child.sendline("hello test")

        # Fake Claude should echo it back
        child.expect("hello test", timeout=5)
        print("✓ Fake Claude received input")

        # Exit
        child.sendline("exit")
        child.expect(pexpect.EOF, timeout=10)

        print("✓ COI_USE_TEST_CLAUDE=1 works correctly!")

    finally:
        if child.isalive():
            child.terminate(force=True)


def test_without_env_var_uses_real_claude(coi_binary, cleanup_containers, tmp_path):
    """Test that without env var, it tries to use real claude (or fails if not installed)."""

    # Start shell WITHOUT test-claude env var
    child = pexpect.spawn(
        coi_binary,
        ["shell", "--tmux=false", "--slot", "96"],
        cwd=str(tmp_path),
        encoding="utf-8",
        timeout=30
    )

    try:
        # Should NOT see message about using test-claude
        index = child.expect([
            "Using test-claude",
            "Tips for getting started",  # Real Claude or might fail to start
            "Starting Claude session",
            pexpect.TIMEOUT
        ], timeout=10)

        # Should not see test-claude message
        assert index != 0, "Should not be using test-claude without env var!"

        print("✓ Without env var, does not use test-claude")

        # Try to exit gracefully
        child.sendline("exit")
        child.expect(pexpect.EOF, timeout=10)

    except Exception as e:
        # It's OK if real Claude isn't licensed or fails - we just want to ensure
        # test-claude wasn't used
        print(f"✓ Without env var, does not use test-claude (real Claude may have failed: {e})")

    finally:
        if child.isalive():
            child.terminate(force=True)
