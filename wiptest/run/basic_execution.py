"""
Tests for coi run command - basic execution.
"""

import subprocess
import time

def test_run_simple_command(coi_binary, cleanup_containers):
    """Test running a simple command in ephemeral container."""
    result = subprocess.run(
        [coi_binary, "run", "--", "echo", "hello world"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Run failed: {result.stderr}"
    assert "hello world" in result.stdout, "Output not captured"


def test_run_with_exit_code(coi_binary, cleanup_containers):
    """Test that run propagates exit codes."""
    # Command that exits with code 42
    result = subprocess.run(
        [coi_binary, "run", "--", "sh", "-c", "exit 42"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 42, f"Expected exit code 42, got {result.returncode}"


def test_run_with_arguments(coi_binary, cleanup_containers):
    """Test running command with multiple arguments."""
    result = subprocess.run(
        [coi_binary, "run", "--", "sh", "-c", "echo $1 $2", "sh", "arg1", "arg2"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "arg1 arg2" in result.stdout
