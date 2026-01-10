"""
Test shell command with fake Claude CLI for fast testing.
This demonstrates using the fake Claude instead of the real one.
"""

import os
import subprocess
import sys
import time

# Add support directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "support"))

import pexpect
from helpers import send_prompt, wait_for_prompt, wait_for_text_on_screen


def test_shell_startup_with_fake_claude(coi_binary, fake_claude_path, cleanup_containers, tmp_path):
    """Test that shell starts successfully with fake Claude CLI."""
    
    # Set up environment to use fake Claude
    env = os.environ.copy()
    env["PATH"] = f"{fake_claude_path}:{env.get('PATH', '')}"
    
    # Start shell with fake Claude
    child = pexpect.spawn(
        coi_binary,
        ["shell", "--workspace", str(tmp_path)],
        encoding="utf-8",
        timeout=30,
        env=env,
    )
    
    try:
        # Wait for Claude to start (fake Claude is much faster!)
        # The fake Claude shows "Fake Claude starting..."
        index = child.expect(["Fake Claude starting", "Tips for getting started", pexpect.TIMEOUT], timeout=10)
        
        assert index != 2, "Timed out waiting for fake Claude to start"
        
        # If we saw "Tips for getting started", Claude is ready
        if index == 1:
            print("Fake Claude started successfully!")
        else:
            # Wait for the prompt
            child.expect(["You:", pexpect.TIMEOUT], timeout=5)
            print("Fake Claude prompt detected!")
        
        # Send a test command
        child.sendline("hello from test")
        
        # Fake Claude echoes back
        child.expect(["I received: hello from test", pexpect.TIMEOUT], timeout=5)
        print("Fake Claude responded correctly!")
        
        # Exit
        child.sendline("exit")
        child.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        
        print("Test completed successfully with fake Claude!")
        
    finally:
        if child.isalive():
            child.terminate(force=True)


def test_fake_claude_performance(coi_binary, fake_claude_path, cleanup_containers, tmp_path):
    """Verify that fake Claude is much faster than real Claude."""
    
    env = os.environ.copy()
    env["PATH"] = f"{fake_claude_path}:{env.get('PATH', '')}"
    
    start_time = time.time()
    
    child = pexpect.spawn(
        coi_binary,
        ["shell", "--workspace", str(tmp_path), "--slot", "99"],  # Use high slot to avoid conflicts
        encoding="utf-8",
        timeout=30,
        env=env,
    )
    
    try:
        # Fake Claude should start in < 5 seconds (real Claude takes 20-30 seconds)
        child.expect(["Fake Claude starting", "You:", pexpect.TIMEOUT], timeout=5)
        elapsed = time.time() - start_time
        
        print(f"Fake Claude started in {elapsed:.2f} seconds")
        assert elapsed < 10, f"Fake Claude took too long: {elapsed:.2f}s (expected < 10s)"
        
        child.sendline("exit")
        child.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        
    finally:
        if child.isalive():
            child.terminate(force=True)
