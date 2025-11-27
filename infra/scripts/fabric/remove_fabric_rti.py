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

def print_summary(solution_name: str, solution_suffix: str, removal_results: dict, failed_steps: list = None):
    """Print final removal summary."""
    any_failures = bool(failed_steps)
    status_icon = "⚠️" if any_failures else "🎉"
    status_text = "REMOVAL COMPLETED WITH WARNINGS" if any_failures else "REMOVAL COMPLETE"
    
    print(f"\n" + "="*60)
    print(f"{status_icon} {solution_name.upper()} {status_text}!")
    print(f"="*60)
    print(f"📅 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏷️  Solution: {solution_suffix}")
    
    # Count successful removals
    removed_items = [item for item, success in removal_results.items() if success]
    failed_items = [item for item, success in removal_results.items() if not success]
    
    if removed_items:
        print(f"\n✅ SUCCESSFULLY REMOVED:")
        for item in removed_items:
            print(f"   🗑️ {item}")
    
    if failed_items:
        print(f"\n❌ FAILED TO REMOVE:")
        for item in failed_items:
            print(f"   ⚠️ {item}")
    
    if not any_failures:
        print(f"\n✨ All targeted resources have been successfully removed!")
    else:
        print(f"\n💡 Some items could not be removed. Please check the warnings above.")
        print(f"   You may need to manually remove failed items or re-run the script.")
    print(f"="*60)

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
    failed_steps = []
    removal_results = {
        'Connection': False,
        'Workspace': False
    }
    
    # Step 1: Authenticate Fabric API client
    fabric_client = fabric_rti_authenticate(step_num=1, total_steps=4)
    if fabric_client is None:
        print(f"\n❌ Authentication failed. Cannot proceed with workspace removal.")
        sys.exit(1)
    executed_steps.append("fabric_rti_authenticate")
    
    # Step 2: Look up workspace by name
    lookup_result = fabric_rti_lookup_workspace(
        fabric_client,
        step_num=2, total_steps=4,
        workspace_name=workspace_name
    )
    if lookup_result is None:
        print("⚠️ Warning: Could not find workspace. Continuing with connection cleanup...")
        failed_steps.append("fabric_rti_lookup_workspace")
        workspace_id = None
        workspace_display_name = workspace_name
    else:
        executed_steps.append("fabric_rti_lookup_workspace")
        workspace_id, workspace_display_name = lookup_result
    
    # Step 3: Delete Event Hub connection
    try:
        connection_result = fabric_rti_delete_connection(
            fabric_client,
            step_num=3, total_steps=4,
            connection_name=connection_name
        )
        if connection_result is not None:
            print(f"Connection deleted successfully: {connection_result}")
            executed_steps.append("fabric_rti_delete_connection")
            removal_results['Connection'] = True
        else:
            print("⚠️ Warning: Connection not found, nothing to delete.")
            executed_steps.append("fabric_rti_delete_connection")
            removal_results['Connection'] = False
    except Exception as e:
        print(f"⚠️ Warning: Could not delete connection: {e}. Continuing with workspace deletion...")
        failed_steps.append("fabric_rti_delete_connection")
        removal_results['Connection'] = False
    
    # Step 4: Delete workspace (only if we found it)
    if workspace_id:
        try:
            result = fabric_rti_delete_workspace(
                fabric_client,
                step_num=4, total_steps=4,
                workspace_id=workspace_id
            )
            if result is not None:
                print(f"Workspace deleted successfully: {result}")
                executed_steps.append("fabric_rti_delete_workspace")
                removal_results['Workspace'] = True
            else:
                print("⚠️ Warning: Workspace not found during deletion, nothing to delete.")
                executed_steps.append("fabric_rti_delete_workspace")
                removal_results['Workspace'] = True
        except Exception as e:
            print(f"⚠️ Warning: Could not delete workspace: {e}")
            failed_steps.append("fabric_rti_delete_workspace")
            removal_results['Workspace'] = False
    else:
        print("⚠️ Skipping workspace deletion (workspace not found)")
        removal_results['Workspace'] = False
    
    # Print final summary
    print_summary(solution_name, solution_suffix, removal_results, failed_steps)

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
