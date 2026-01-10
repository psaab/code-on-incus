"""
Test that sudo works correctly for the claude user.

Verifies that:
1. sudo can be run without password
2. sudoers file has correct ownership (root:root)
3. sudoers file has correct permissions (440)
"""

import subprocess
import json


def test_sudo_works(coi_binary, cleanup_containers, tmp_path):
    """Test that sudo works without password."""

    # Run command that tests sudo
    result = subprocess.run(
        [coi_binary, "run", "sudo", "whoami"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=30
    )

    assert result.returncode == 0, f"sudo command failed: {result.stderr}"
    assert "root" in result.stdout, f"Expected 'root' in output, got: {result.stdout}"

    print("✓ sudo works without password")


def test_sudoers_file_ownership(coi_binary, cleanup_containers, tmp_path):
    """Test that sudoers file has correct ownership (root:root)."""

    # Check sudoers file ownership
    result = subprocess.run(
        [coi_binary, "run", "--", "stat", "-c", "%U:%G %a", "/etc/sudoers.d/claude"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=30
    )

    assert result.returncode == 0, f"Failed to check sudoers ownership: {result.stderr}"

    # Parse output: should be "root:root 440"
    output = result.stdout.strip()
    parts = output.split()

    assert len(parts) == 2, f"Unexpected output format: {output}"
    ownership = parts[0]
    permissions = parts[1]

    assert ownership == "root:root", f"Expected root:root ownership, got: {ownership}"
    assert permissions == "440", f"Expected 440 permissions, got: {permissions}"

    print(f"✓ sudoers file has correct ownership: {ownership} {permissions}")


def test_sudo_no_password_required(coi_binary, cleanup_containers, tmp_path):
    """Test that sudo doesn't require password for claude user."""

    # Try running sudo command - should work without password
    result = subprocess.run(
        [coi_binary, "run", "--", "sudo", "-n", "whoami"],  # -n = non-interactive, fail if password required
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=30
    )

    assert result.returncode == 0, f"sudo -n failed (password required?): {result.stderr}"
    assert "root" in result.stdout, f"Expected 'root' in output, got: {result.stdout}"

    print("✓ sudo works non-interactively (no password required)")
