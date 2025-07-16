#!/usr/bin/env python3
"""
🧪 Test Runner for Gestão Tattoo Studio

This script runs all tests for the Tattoo Studio Management System.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n🔄 {description}")
    print("=" * 60)
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            print(result.stdout)
        else:
            print(f"❌ {description} - FAILED")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 GESTÃO TATTOO STUDIO - TEST SUITE")
    print("=" * 60)

    # Change to project directory
    project_dir = Path(__file__).parent.parent
    print(f"📁 Working directory: {project_dir}")

    # Tests to run
    tests = [
        ("python tests/test_data.py", "Generate Test Data"),
        ("python -m pytest tests/test_utils.py -v", "Utility Tests"),
        ("python -m pytest tests/test_models.py -v", "Model Tests"),
        ("python -m pytest tests/test_routes.py -v", "Route Tests"),
        ("python -m pytest tests/ -v --tb=short", "All Tests Combined"),
    ]

    successful_tests = 0
    total_tests = len(tests)

    for command, description in tests:
        full_command = f"cd {project_dir} && {command}"
        if run_command(full_command, description):
            successful_tests += 1

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {successful_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - successful_tests}/{total_tests}")

    if successful_tests == total_tests:
        print("🎉 All tests passed successfully!")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
