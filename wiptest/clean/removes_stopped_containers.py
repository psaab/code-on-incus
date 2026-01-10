"""
Test that clean command removes stopped test containers.

Flow:
1. Create a test container with recognizable name pattern (coi-test-*)
2. Stop the container
3. Run coi clean --force
4. Verify test container is removed

Expected:
- Stopped test containers are cleaned
- Clean operation succeeds
"""

import subprocess
import time
import uuid


def test_clean_removes_stopped_test_containers(coi_binary):
    """Test that clean removes stopped containers with coi-test prefix."""
    # Create a unique test container name
    test_id = str(uuid.uuid4())[:8]
    test_container = f"coi-test-clean-{test_id}"

    try:
        # Create a test container (using ubuntu base)
        create_result = subprocess.run(
            ["incus", "launch", "images:ubuntu/22.04", test_container],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if create_result.returncode != 0:
            # If we can't create test container, skip test
            print(f"Skipping: Cannot create test container: {create_result.stderr}")
            return

        # Give it a moment to start
        time.sleep(2)

        # Stop the container
        stop_result = subprocess.run(
            ["incus", "stop", test_container],
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert stop_result.returncode == 0, f"Failed to stop container: {stop_result.stderr}"

        # Verify container exists and is stopped
        list_result = subprocess.run(
            ["incus", "list", test_container, "--format=csv"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert test_container in list_result.stdout, "Test container should exist"
        assert "STOPPED" in list_result.stdout, "Test container should be stopped"

        # Run clean with force flag
        clean_result = subprocess.run(
            [coi_binary, "clean", "--force"], capture_output=True, text=True, timeout=30
        )

        # Clean should succeed (exit 0)
        assert clean_result.returncode == 0, f"Clean failed: {clean_result.stderr}"

        # Give cleanup a moment
        time.sleep(2)

        # Verify test container is removed
        list_after = subprocess.run(
            ["incus", "list", test_container, "--format=csv"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Container should be gone (empty output or not found)
        assert test_container not in list_after.stdout, (
            "Test container should be removed after clean"
        )

    finally:
        # Cleanup: Force delete test container if it still exists
        subprocess.run(
            ["incus", "delete", "-f", test_container],
            capture_output=True,
            timeout=30,
        )
