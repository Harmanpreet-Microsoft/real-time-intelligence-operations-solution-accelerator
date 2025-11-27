#!/usr/bin/env python3
"""
Fabric Authentication Module

This module provides authentication functionality for Microsoft Fabric API operations.

Usage:
    python fabric_auth.py

Requirements:
    - fabric_api.py module in the same directory
    - Azure CLI authentication or other Azure credentials configured
"""

import argparse
import sys
from fabric_api import FabricApiClient

def authenticate():
    """
    Authenticate and create Fabric API client.
    
    Returns:
        Authenticated FabricApiClient instance if successful, None if failed
    """
    try:
        result = FabricApiClient()
        print(f"✅ Successfully authenticated Fabric API client")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main function to handle command line arguments and execute authentication."""
    parser = argparse.ArgumentParser(
        description="Test Fabric API authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fabric_auth.py
        """
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the main logic
    result = authenticate()
    
    print(f"\n✅ Authentication: {'Success' if result else 'Failed'}")


if __name__ == "__main__":
    main()