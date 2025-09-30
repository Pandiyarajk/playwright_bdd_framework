#!/usr/bin/env python
"""
Example demonstrating powerlogger usage in the automation framework.
This shows various logging patterns with emoji support.
"""

from powerlogger import get_logger

logger = get_logger("powerlogger_example")


def demonstrate_basic_logging():
    """Demonstrate basic logging levels with emojis."""
    logger.info("🚀 Starting application")
    logger.debug("🔍 Debug information - detailed processing data")
    logger.info("✅ Operation completed successfully")
    logger.warning("⚠️ Warning: Resource usage is high")
    logger.error("❌ Error occurred during processing")


def demonstrate_application_workflow():
    """Simulate a typical application workflow."""
    logger.info("🚀 Starting application")
    
    try:
        # Simulating initialization
        logger.info("⚙️ Initializing configuration...")
        logger.debug("🔍 Loading config from file")
        logger.info("✅ Configuration loaded successfully")
        
        # Simulating main logic
        logger.info("📋 Processing user input...")
        logger.debug("🔍 Validating input data")
        logger.info("✅ Input validation passed")
        
        logger.info("💾 Saving data to database...")
        logger.debug("🔍 Executing SQL query")
        logger.info("✅ Data saved successfully")
        
        logger.info("✅ Application running successfully")
        
    except Exception as e:
        logger.error(f"❌ Application error: {e}")
        logger.exception("📋 Full traceback:")
    
    logger.info("🏁 Application finished")


def demonstrate_test_execution():
    """Simulate test execution logging."""
    logger.info("=" * 80)
    logger.info("🚀 STARTING TEST EXECUTION")
    logger.info("=" * 80)
    
    # Test Case 1
    logger.info("\n🎬 SCENARIO: User Login")
    logger.info("🏷️ Tags: smoke, authentication")
    logger.debug("🔍 STEP: Navigate to login page")
    logger.debug("🔍 STEP: Enter credentials")
    logger.debug("🔍 STEP: Click login button")
    logger.info("✅ SCENARIO PASSED: User Login")
    logger.info("⏱️ Duration: 2.45s")
    
    # Test Case 2
    logger.info("\n🎬 SCENARIO: Data Upload")
    logger.info("🏷️ Tags: regression, data")
    logger.debug("🔍 STEP: Select file")
    logger.debug("🔍 STEP: Upload file")
    logger.error("❌ STEP FAILED: Verify upload")
    logger.error("❌ SCENARIO FAILED: Data Upload")
    logger.info("⏱️ Duration: 5.12s")
    logger.info("📸 Screenshot saved: failure_data_upload_20250930.png")
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("📋 TEST EXECUTION SUMMARY")
    logger.info("=" * 80)
    logger.info("📊 Total Scenarios: 2")
    logger.info("✅ Passed: 1")
    logger.info("❌ Failed: 1")
    logger.info("⏭️ Skipped: 0")
    logger.info("⏱️ Duration: 7.57s")
    logger.info("=" * 80)


def demonstrate_integration_logging():
    """Demonstrate logging for external integrations."""
    logger.info("🔗 Initializing Jira integration")
    logger.info("✅ Connected to Jira: https://company.atlassian.net")
    
    logger.info("🔗 Initializing Zephyr Scale integration")
    logger.info("✅ Zephyr Scale integration initialized")
    
    logger.info("📊 System monitoring started")
    logger.info("📧 Email report sent")
    
    logger.info("🛑 System monitoring stopped")


def demonstrate_error_handling():
    """Demonstrate error handling and exception logging."""
    logger.info("🚀 Starting error handling demo")
    
    try:
        logger.debug("🔍 Processing complex operation...")
        # Simulate an error
        raise ValueError("Invalid configuration parameter")
        
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.exception("📋 Full traceback:")
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        logger.exception("📋 Full traceback:")
        
    finally:
        logger.info("🧹 Cleanup completed")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 80)
    print("POWERLOGGER DEMONSTRATION")
    print("=" * 80 + "\n")
    
    print("\n1. Basic Logging:")
    print("-" * 40)
    demonstrate_basic_logging()
    
    print("\n\n2. Application Workflow:")
    print("-" * 40)
    demonstrate_application_workflow()
    
    print("\n\n3. Test Execution:")
    print("-" * 40)
    demonstrate_test_execution()
    
    print("\n\n4. Integration Logging:")
    print("-" * 40)
    demonstrate_integration_logging()
    
    print("\n\n5. Error Handling:")
    print("-" * 40)
    demonstrate_error_handling()
    
    print("\n" + "=" * 80)
    print("🏁 DEMONSTRATION COMPLETE")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
