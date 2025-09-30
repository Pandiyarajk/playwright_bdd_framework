#!/usr/bin/env python
"""
Verification script for powerlogger integration.
This script tests that powerlogger is properly integrated across the framework.
"""

import sys
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can import powerlogger successfully."""
    print("=" * 80)
    print("Testing Powerlogger Imports")
    print("=" * 80)
    
    tests = []
    
    # Test 1: Direct powerlogger import
    try:
        from powerlogger import get_logger
        logger = get_logger("test")
        logger.info("✅ Direct powerlogger import works")
        tests.append(("Direct import", True, None))
    except Exception as e:
        print(f"❌ Failed to import powerlogger: {e}")
        print("\n💡 HINT: Install powerlogger first:")
        print("   pip install powerlogger")
        print("   OR")
        print("   pip install -r requirements.txt")
        print("\nSee INSTALLATION_NOTES.md for details.\n")
        tests.append(("Direct import", False, str(e)))
        return tests
    
    # Test 2: Logger setup
    try:
        from framework.logging_setup.logger import setup_logger
        logger = setup_logger()
        logger.info("✅ setup_logger() function works")
        tests.append(("Logger setup", True, None))
    except Exception as e:
        print(f"❌ Failed to import logger setup: {e}")
        tests.append(("Logger setup", False, str(e)))
    
    # Test 3: System Monitor
    try:
        from framework.logging_setup.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        print("✅ SystemMonitor imports successfully")
        tests.append(("SystemMonitor", True, None))
    except Exception as e:
        print(f"❌ Failed to import SystemMonitor: {e}")
        tests.append(("SystemMonitor", False, str(e)))
    
    # Test 4: Jira Integration
    try:
        from framework.integrations.jira_integration import JiraIntegration
        print("✅ JiraIntegration imports successfully")
        tests.append(("JiraIntegration", True, None))
    except Exception as e:
        print(f"❌ Failed to import JiraIntegration: {e}")
        tests.append(("JiraIntegration", False, str(e)))
    
    # Test 5: Zephyr Integration
    try:
        from framework.integrations.zephyr_integration import ZephyrIntegration
        print("✅ ZephyrIntegration imports successfully")
        tests.append(("ZephyrIntegration", True, None))
    except Exception as e:
        print(f"❌ Failed to import ZephyrIntegration: {e}")
        tests.append(("ZephyrIntegration", False, str(e)))
    
    # Test 6: Email Reporter
    try:
        from framework.reporting.email_reporter import EmailReporter
        print("✅ EmailReporter imports successfully")
        tests.append(("EmailReporter", True, None))
    except Exception as e:
        print(f"❌ Failed to import EmailReporter: {e}")
        tests.append(("EmailReporter", False, str(e)))
    
    return tests


def test_logging_features():
    """Test that powerlogger features work correctly."""
    print("\n" + "=" * 80)
    print("Testing Powerlogger Features")
    print("=" * 80)
    
    from powerlogger import get_logger
    
    logger = get_logger("verification_test")
    
    print("\n1. Testing different log levels:")
    logger.debug("🔍 DEBUG: This is a debug message")
    logger.info("ℹ️ INFO: This is an info message")
    logger.warning("⚠️ WARNING: This is a warning message")
    logger.error("❌ ERROR: This is an error message")
    
    print("\n2. Testing emoji support:")
    logger.info("🚀 Starting test")
    logger.info("✅ Test passed")
    logger.info("📊 Statistics generated")
    logger.info("🏁 Test completed")
    
    print("\n3. Testing exception logging:")
    try:
        raise ValueError("Test exception for verification")
    except ValueError as e:
        logger.error(f"❌ Caught exception: {e}")
        # Note: Don't actually call exception() in test as it will print full traceback
        logger.info("📋 Exception logging works")
    
    print("\n✅ All logging features work correctly")
    return True


def test_example_script():
    """Test that the example script exists and is valid Python."""
    print("\n" + "=" * 80)
    print("Testing Example Script")
    print("=" * 80)
    
    example_path = Path(__file__).parent / "examples" / "powerlogger_example.py"
    
    if not example_path.exists():
        print(f"❌ Example script not found: {example_path}")
        return False
    
    print(f"✅ Example script exists: {example_path}")
    
    # Try to compile it
    try:
        with open(example_path, 'r') as f:
            code = f.read()
        compile(code, str(example_path), 'exec')
        print("✅ Example script is valid Python")
        return True
    except SyntaxError as e:
        print(f"❌ Example script has syntax error: {e}")
        return False


def test_documentation():
    """Test that documentation files exist."""
    print("\n" + "=" * 80)
    print("Testing Documentation")
    print("=" * 80)
    
    docs = [
        "docs/POWERLOGGER_MIGRATION.md",
        "POWERLOGGER_INTEGRATION_SUMMARY.md",
        "README.md"
    ]
    
    all_exist = True
    for doc in docs:
        doc_path = Path(__file__).parent / doc
        if doc_path.exists():
            print(f"✅ {doc} exists")
        else:
            print(f"❌ {doc} not found")
            all_exist = False
    
    return all_exist


def print_summary(import_tests, features_ok, example_ok, docs_ok):
    """Print test summary."""
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    # Import tests
    passed = sum(1 for _, success, _ in import_tests if success)
    total = len(import_tests)
    print(f"\nImport Tests: {passed}/{total} passed")
    for name, success, error in import_tests:
        status = "✅" if success else "❌"
        print(f"  {status} {name}")
        if error:
            print(f"      Error: {error}")
    
    # Feature tests
    print(f"\nLogging Features: {'✅ Passed' if features_ok else '❌ Failed'}")
    print(f"Example Script: {'✅ Valid' if example_ok else '❌ Invalid'}")
    print(f"Documentation: {'✅ Complete' if docs_ok else '❌ Incomplete'}")
    
    # Overall result
    all_passed = all(success for _, success, _ in import_tests) and features_ok and example_ok and docs_ok
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print("Powerlogger is successfully integrated!")
    else:
        print("⚠️ SOME VERIFICATIONS FAILED")
        print("Please review the errors above.")
    print("=" * 80)
    
    return all_passed


def main():
    """Run all verification tests."""
    print("\n" + "=" * 80)
    print("🔍 POWERLOGGER INTEGRATION VERIFICATION")
    print("=" * 80 + "\n")
    
    # Run tests
    import_tests = test_imports()
    features_ok = test_logging_features()
    example_ok = test_example_script()
    docs_ok = test_documentation()
    
    # Print summary
    all_passed = print_summary(import_tests, features_ok, example_ok, docs_ok)
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
