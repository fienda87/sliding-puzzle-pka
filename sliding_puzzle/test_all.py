"""
Run all tests to verify 4x4 grid support implementation
"""
import sys
import subprocess


def run_test(test_file, description):
    """Run a test file and report results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"File: {test_file}")
    print('='*60)
    
    result = subprocess.run(
        [sys.executable, test_file],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"❌ FAILED: {test_file}")
        print(result.stderr)
        return False
    else:
        print(f"✅ PASSED: {test_file}")
        return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("COMPREHENSIVE TEST SUITE FOR 4x4 GRID SUPPORT")
    print("="*60)
    
    tests = [
        ("test_quick.py", "Quick Smoke Test"),
        ("test_4x4.py", "4x4 Grid Functionality Tests"),
        ("test_difficulty_presets.py", "Difficulty Presets Integration Tests"),
    ]
    
    results = []
    
    for test_file, description in tests:
        passed = run_test(test_file, description)
        results.append((test_file, description, passed))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_file, description, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {description}")
    
    all_passed = all(passed for _, _, passed in results)
    
    if all_passed:
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED! 4x4 GRID SUPPORT READY!")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("❌ SOME TESTS FAILED")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
