#!/usr/bin/env python3
"""
Workspace removal orchestrator script for Real-Time Intelligence Operations Solution Accelerator.

This script coordinates the execution of workspace removal functions
in the correct order, with proper error handling and logging. It uses environment
variables for configuration and calls each function directly.

Functions executed in order:
1. fabric_rti_authenticate - Authenticate Fabric API client
2. fabric_rti_lookup_workspace - Look up workspace by name
3. fabric_rti_delete_connection - Delete Event Hub connection
4. fabric_rti_delete_workspace - Delete the Fabric workspace

Usage:
    python remove_fabric_rti.py

Environment Variables (from Bicep outputs):
    AZURE_ENV_NAME - Name of the Azure environment
    SOLUTION_SUFFIX - Required suffix to append to default workspace name
    FABRIC_WORKSPACE_NAME - Name of the Fabric workspace (optional, uses default if not provided)
    FABRIC_EVENT_HUB_CONNECTION_NAME - Name of the Event Hub connection (optional, uses default if not provided)
"""

import os
import sys
from datetime import datetime

# Add current directory to path so we can import local modules
sys.path.append(os.path.dirname(__file__))

# Import removal functions
from fabric_rti_helper import fabric_rti_authenticate, fabric_rti_lookup_workspace, fabric_rti_delete_connection, fabric_rti_delete_workspace, get_required_env_var

def print_summary(executed_steps: list, failed_step: str = None):
    """Print execution summary."""
    print("\n" + "="*60)
    print("📊 EXECUTION SUMMARY")
    print("="*60)
    
    if executed_steps:
        print("✅ Successfully executed functions:")
        for step in executed_steps:
            print(f"   ✓ {step}")
    
    if failed_step:
        print(f"\n❌ Failed at function: {failed_step}")
        print(f"\n💡 To resume from failed point, fix the issue and re-run the remove_fabric_rti.py script")
    else:
        print(f"\n🎉 All {len(executed_steps)} functions completed successfully!")

def main():
    # Calculate repository root directory (3 levels up from this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    
    # Load configuration from environment variables
    solution_name = get_required_env_var("AZURE_ENV_NAME")
    solution_suffix = get_required_env_var("SOLUTION_SUFFIX")
    workspace_name = os.getenv("FABRIC_WORKSPACE_NAME", f"Real-Time Intelligence for Operations - {solution_suffix}")
    connection_name = os.getenv("FABRIC_EVENT_HUB_CONNECTION_NAME", f"rti_eventhub_connection_{solution_suffix}")

    # Show removal summary
    print(f"🏭 {solution_name} Workspace Removal")
    print("="*60)
    print(f"Target workspace name: {workspace_name}")
    print(f"Target connection name: {connection_name}")
    print(f"Solution Suffix: {solution_suffix}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    executed_steps = []
    
    # Step 1: Authenticate Fabric API client
    fabric_client = fabric_rti_authenticate(step_num=1, total_steps=4)
    if fabric_client is None:
        print_summary(executed_steps, failed_step="fabric_rti_authenticate")
        sys.exit(1)
    executed_steps.append("fabric_rti_authenticate")
    
    # Step 2: Look up workspace by name
    lookup_result = fabric_rti_lookup_workspace(
        fabric_client,
        step_num=2, total_steps=4,
        workspace_name=workspace_name
    )
    if lookup_result is None:
        print_summary(executed_steps, failed_step="fabric_rti_lookup_workspace")
        sys.exit(1)
    executed_steps.append("fabric_rti_lookup_workspace")
    workspace_id, workspace_display_name = lookup_result
    
    # Step 3: Delete Event Hub connection
    connection_result = fabric_rti_delete_connection(
        fabric_client,
        step_num=3, total_steps=4,
        connection_name=connection_name
    )
    if connection_result is None:
        print_summary(executed_steps, failed_step="fabric_rti_delete_connection")
        sys.exit(1)
    executed_steps.append("fabric_rti_delete_connection")
    
    # Step 4: Delete workspace
    result = fabric_rti_delete_workspace(
        fabric_client,
        step_num=4, total_steps=4,
        workspace_id=workspace_id
    )
    if result is None:
        print_summary(executed_steps, failed_step="fabric_rti_delete_workspace")
        sys.exit(1)
    executed_steps.append("fabric_rti_delete_workspace")
    
    # Success!
    print(f"\n🎉 {solution_name} workspace removal completed successfully!")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print_summary(executed_steps)

    print(f"\n" + "="*60)
    print(f"🎉 {solution_name.upper()} WORKSPACE REMOVAL COMPLETE!")
    print(f"="*60)
    print(f"📅 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏷️  Solution: {solution_suffix}")
    print(f"\n🗑️  DELETED RESOURCE:")
    print(f"   🏠 Workspace: {workspace_display_name}")
    print(f"   🆔 ID:        {workspace_id}")
    print(f"\n✨ Your workspace has been successfully removed!")
    print(f"="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⚠️ Workspace removal interrupted by user")
        sys.exit(1)
    except UnicodeEncodeError as e:
        print(f"\n[ERROR] Unicode encoding error detected:")
        print(f"Your console doesn't support the Unicode characters used in this script.")
        print(f"This is common on Windows systems with certain console configurations.")
        print(f"\nSolutions:")
        print(f"1. Run the script in Windows Terminal or VS Code terminal")
        print(f"2. Use PowerShell 7+ instead of Windows PowerShell")
        print(f"3. Set environment variable: set PYTHONIOENCODING=utf-8")
        print(f"4. Use command: chcp 65001 (to set UTF-8 codepage)")
        print(f"\nTechnical details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)
