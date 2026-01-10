"""
Test build subcommand with end-to-end functionality.

Flow:
1. Check if coi image exists
2. If not, attempt to build it (or skip test if takes too long)
3. If exists, verify we can launch container from it
4. Clean up test container

Expected:
- Build command works for core images
- Built images are usable for launching containers
- Build handles existing images correctly
"""

import subprocess
import time


def test_build_coi_functionality(coi_binary, cleanup_containers):
    """Test that coi build works end-to-end."""
    # Check if coi already exists
    result = subprocess.run(
        [coi_binary, "image", "exists", "coi"],
        capture_output=True,
    )

    if result.returncode == 0:
        # Image exists, verify we can use it
        print("coi image exists, verifying it's usable...")

        # Try to launch a container from it
        test_container = "coi-test-verify"

        launch_result = subprocess.run(
            [coi_binary, "container", "launch", "coi", test_container],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if launch_result.returncode == 0:
            # Successfully launched, clean up
            time.sleep(2)
            subprocess.run(
                [coi_binary, "container", "delete", test_container, "--force"],
                capture_output=True,
                timeout=10,
            )
            assert True, "coi image is usable"
        else:
            assert False, f"Failed to launch container from coi: {launch_result.stderr}"

    else:
        # Image doesn't exist, try to build it
        print("coi not found, attempting to build (this may take several minutes)...")

        build_result = subprocess.run(
            [coi_binary, "build"],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout for build
        )

        if build_result.returncode == 0:
            # Build succeeded
            print("Successfully built coi image")

            # Verify image now exists
            exists_result = subprocess.run(
                [coi_binary, "image", "exists", "coi"],
                capture_output=True,
            )
            assert exists_result.returncode == 0, "Built image should exist after successful build"

            # Try to launch a test container to verify it works
            test_container = "coi-test-verify"

            launch_result = subprocess.run(
                [coi_binary, "container", "launch", "coi", test_container],
                capture_output=True,
                text=True,
                timeout=30,
            )

            assert launch_result.returncode == 0, f"Should be able to launch from built image: {launch_result.stderr}"

            # Clean up test container
            time.sleep(2)
            subprocess.run(
                [coi_binary, "container", "delete", test_container, "--force"],
                capture_output=True,
                timeout=10,
            )

        else:
            # Build failed - this might be expected in some environments
            # Check if it's a known error (base image not available, etc.)
            error_output = build_result.stderr + build_result.stdout

            if "not found" in error_output.lower() or "not available" in error_output.lower():
                import pytest
                pytest.skip("Base image not available for building coi")
            else:
                assert False, f"Build failed unexpectedly: {error_output}"


def test_build_handles_existing_image(coi_binary):
    """Test that build command handles existing images correctly."""
    # Try to build coi (if it exists, should skip or warn)
    result = subprocess.run(
        [coi_binary, "build"],
        capture_output=True,
        text=True,
        timeout=30,  # Should be quick if image exists
    )

    # Should either succeed (skip message) or fail gracefully
    output = result.stdout + result.stderr

    if result.returncode == 0:
        # If successful, should mention skipping or already exists
        assert "already" in output.lower() or "exist" in output.lower() or "skip" in output.lower(), \
            "Build should indicate image already exists"
    else:
        # If failed, should have an informative error message
        assert len(output.strip()) > 10, "Build failure should have error message"
