#!/usr/bin/env python
"""
Test execution script with various options.
Provides convenient command-line interface for running tests.
"""

import sys
import os
import argparse
from pathlib import Path
from powerlogger import get_logger

logger = get_logger("test_runner")


def main():
    """Main execution entry point."""
    logger.info("🚀 Starting test execution script")
    
    parser = argparse.ArgumentParser(
        description='Playwright Python BDD Test Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python run_tests.py
  
  # Run tests with specific tags
  python run_tests.py --tags smoke
  python run_tests.py --tags "smoke and regression"
  
  # Run specific feature
  python run_tests.py --feature features/example.feature
  
  # Run with specific browser
  python run_tests.py --browser firefox
  
  # Run in headless mode
  python run_tests.py --headless
  
  # Generate Allure report
  python run_tests.py --allure
  
  # Parallel execution
  python run_tests.py --parallel 4
        """
    )
    
    parser.add_argument(
        '--tags',
        '-t',
        help='Run scenarios matching tag expression (e.g., "smoke", "smoke and regression")',
        default=None
    )
    
    parser.add_argument(
        '--feature',
        '-f',
        help='Run specific feature file',
        default=None
    )
    
    parser.add_argument(
        '--browser',
        '-b',
        choices=['chromium', 'firefox', 'webkit'],
        help='Browser to use',
        default=None
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run in headless mode'
    )
    
    parser.add_argument(
        '--env',
        '-e',
        help='Environment to run tests in (dev, test, staging, prod)',
        default='test'
    )
    
    parser.add_argument(
        '--allure',
        action='store_true',
        help='Generate Allure report'
    )
    
    parser.add_argument(
        '--parallel',
        '-p',
        type=int,
        help='Number of parallel workers',
        default=1
    )
    
    parser.add_argument(
        '--stop-on-failure',
        action='store_true',
        help='Stop execution on first failure'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run (validate scenarios without executing)'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ['ENV'] = args.env
    
    if args.browser:
        os.environ['BROWSER'] = args.browser
    
    if args.headless:
        os.environ['HEADLESS'] = 'true'
    
    # Build behave command
    cmd_parts = ['behave']
    
    # Add tags
    if args.tags:
        cmd_parts.extend(['--tags', args.tags])
    
    # Add feature file
    if args.feature:
        cmd_parts.append(args.feature)
    
    # Add format
    if args.verbose:
        cmd_parts.extend(['--format', 'plain'])
    else:
        cmd_parts.extend(['--format', 'pretty'])
    
    # Add Allure formatter
    if args.allure:
        cmd_parts.extend([
            '--format', 'allure_behave.formatter:AllureFormatter',
            '--outfile', 'allure-results'
        ])
    
    # Add stop on failure
    if args.stop_on_failure:
        cmd_parts.append('--stop')
    
    # Add dry run
    if args.dry_run:
        cmd_parts.append('--dry-run')
    
    # Add parallel execution
    if args.parallel > 1:
        # Note: behave doesn't support parallel execution natively
        # This would require behave-parallel or custom implementation
        print(f"Note: Parallel execution with {args.parallel} workers requires behave-parallel")
        print("Install with: pip install behave-parallel")
        # Uncomment if behave-parallel is installed:
        # cmd_parts.extend(['--processes', str(args.parallel)])
    
    # Execute command
    cmd = ' '.join(cmd_parts)
    logger.info(f"▶️ Executing: {cmd}\n")
    
    exit_code = os.system(cmd)
    
    # Generate Allure report if requested
    if args.allure and exit_code == 0:
        logger.info("\n📊 Generating Allure report...")
        os.system('allure serve allure-results')
    
    if exit_code == 0:
        logger.info("✅ Test execution completed successfully")
    else:
        logger.error("❌ Test execution failed")
    
    logger.info("🏁 Test runner finished")
    sys.exit(exit_code >> 8)


if __name__ == '__main__':
    main()