#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pre-commit Hook Runner for AlgoTradePro5.

This script is called by Git when committing changes and runs the pre-commit hook.
"""

import logging
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the pre-commit hook
from hooks.pre_commit_hook import PreCommitHook

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/pre_commit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("pre_commit_runner")

def main():
    """Main entry point for the pre-commit hook runner."""
    try:
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Create the pre-commit hook
        hook = PreCommitHook()
        
        # Run the pre-commit hook
        success = hook.run_pre_commit_hook()
        
        # Exit with appropriate status code
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Pre-commit hook failed with exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
