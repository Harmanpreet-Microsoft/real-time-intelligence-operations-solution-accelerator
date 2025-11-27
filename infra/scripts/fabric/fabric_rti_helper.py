#!/usr/bin/env python3
"""
Helper functions for Real-Time Intelligence Operations Solution Accelerator
Fabric workspace management.

This module provides utility functions for Fabric Real-Time Intelligence deployment operations.
"""

import os
import sys
from fabric_api import FabricApiClient, FabricApiError

def get_required_env_var(var_name: str) -> str:
    """Get a required environment variable or exit with error.
    
    Args:
        var_name: Name of the environment variable to retrieve
        
    Returns:
        Value of the environment variable
        
    Raises:
        SystemExit: If the environment variable is not set
    """
    value = os.getenv(var_name)
    if not value:
        print(f"❌ Missing required environment variable: {var_name}")
        sys.exit(1)
    return value

def print_step(step_num: int = None, total_steps: int = None, description: str = None, **kwargs):
    """
    Print RTI operation step information.
    
    Args:
        step_num: Optional current step number
        total_steps: Optional total number of steps
        description: Optional description of what this step does
        **kwargs: Arguments for display purposes
    """
    if step_num is not None and total_steps is not None and description:
        print(f"\n📋 Step {step_num}/{total_steps}: {description}")
    elif description:
        print(f"\n📋 {description}")
    
    if kwargs:
        args_str = ", ".join([f"{k}={v}" for k, v in kwargs.items() if "key" not in k.lower()])
        print(f"   Parameters: {args_str}")

def fabric_rti_authenticate(step_num: int = None, total_steps: int = None):
    """
    Authenticate and create Fabric API client.
    
    Args:
        step_num: Optional current step number
        total_steps: Optional total number of steps
        
    Returns:
        Authenticated FabricApiClient instance if successful, None if failed
    """
    print_step(step_num, total_steps, "Authenticating Fabric API client")
    
    try:
        result = FabricApiClient()
        print(f"✅ Successfully completed: fabric_rti_authenticate")
        return result
    except Exception as e:
        print(f"❌ Exception while executing fabric_rti_authenticate: {e}")
        return None

def fabric_rti_lookup_workspace(fabric_client: FabricApiClient, step_num: int = None, total_steps: int = None, workspace_name: str = None):
    """
    Look up workspace by name.
    
    Args:
        fabric_client: Authenticated FabricApiClient instance
        step_num: Optional current step number
        total_steps: Optional total number of steps
        workspace_name: Workspace name to look up
        
    Returns:
        Tuple of (workspace_id, workspace_display_name) if successful, None if failed
    """
    params = {}
    if workspace_name:
        params['workspace_name'] = workspace_name
        
    print_step(step_num, total_steps, "Looking up workspace", **params)
    
    try:
        print(f"Looking up workspace: '{workspace_name}'")
        workspaces = fabric_client.get_workspaces()
        workspace = next(
            (w for w in workspaces if w['displayName'].lower() == workspace_name.lower()), None)
        
        if not workspace:
            print(f"   Workspace '{workspace_name}' not found")
            return None
        
        workspace_id = workspace['id']
        workspace_display_name = workspace['displayName']
        print(f"✅ Found workspace: '{workspace_display_name}' (ID: {workspace_id})")
        result = workspace_id, workspace_display_name
            
        print(f"✅ Successfully completed: fabric_rti_lookup_workspace")
        return result
        
    except FabricApiError as e:
        if e.status_code == 401:
            print(f"⚠️ WARNING: Unauthorized access to Fabric APIs")
            print("   ⚠️ WARNING: Please review your Fabric permissions and licensing:")
            print("   📋 Check these resources:")
            print("   • Fabric licenses: https://learn.microsoft.com/en-us/fabric/enterprise/licenses")
            print("   • Identity support: https://learn.microsoft.com/en-us/rest/api/fabric/articles/identity-support")
            print("   • Create Entra app: https://learn.microsoft.com/en-us/rest/api/fabric/articles/get-started/create-entra-app")
            print("   Solution: Ensure you have proper Fabric licensing and permissions")
        elif e.status_code == 404:
            print(f"WARNING: Resource not found")
        elif e.status_code == 403:
            print(f"⚠️ WARNING: Access denied")
            print("   Solution: Ensure you have appropriate permissions")
        else:
            print(f"⚠️ WARNING: Fabric API error")
        print(f"   Status Code: {e.status_code}")
        print(f"   Details: {str(e)}")
        print(f"❌ Exception while executing fabric_rti_lookup_workspace: {e}")
        return None
    except Exception as e:
        print(f"WARNING: Unexpected error during workspace lookup: {str(e)}")
        print(f"❌ Exception while executing fabric_rti_lookup_workspace: {e}")
        return None

def fabric_rti_delete_connection(fabric_client: FabricApiClient, step_num: int = None, total_steps: int = None, connection_name: str = None):
    """
    Delete Event Hub connection by name.
    
    Args:
        fabric_client: Authenticated FabricApiClient instance
        step_num: Optional current step number
        total_steps: Optional total number of steps
        connection_name: Name of the connection to delete
        
    Returns:
        Connection ID if deletion successful, None if connection not found
        
    Raises:
        FabricApiError: If deletion fails due to unexpected error
    """
    params = {'connection_name': connection_name}
    print_step(step_num, total_steps, "Deleting Event Hub connection", **params)
    
    try:
        print(f"Looking up connection: '{connection_name}'")
        connections = fabric_client.list_connections()
        
        # Find connection by display name
        connection = None
        for conn in connections:
            if conn.get('displayName', '').lower() == connection_name.lower():
                connection = conn
                break
        
        if not connection:
            print(f"Connection '{connection_name}' not found")
            return None
        
        connection_id = connection.get('id')
        print(f"Found connection: '{connection_name}' (ID: {connection_id})")
        
        # Delete the connection
        deleted_connection_id = fabric_client.delete_connection(connection_id)
        if deleted_connection_id:
            print(f"✅ Successfully completed: fabric_rti_delete_connection (deleted: {deleted_connection_id})")
            return deleted_connection_id
        else:
            print(f"Connection {connection_id} was not found during deletion")
            return None
        
    except FabricApiError as e:
        if e.status_code == 401:
            print(f"⚠️ WARNING: Unauthorized access to Fabric APIs")
            print("   ⚠️ WARNING: Please review your Fabric permissions and licensing:")
            print("   📋 Check these resources:")
            print("   • Fabric licenses: https://learn.microsoft.com/en-us/fabric/enterprise/licenses")
            print("   • Identity support: https://learn.microsoft.com/en-us/rest/api/fabric/articles/identity-support")
            print("   • Create Entra app: https://learn.microsoft.com/en-us/rest/api/fabric/articles/get-started/create-entra-app")
            print("   Solution: Ensure you have proper Fabric licensing and permissions")
        elif e.status_code == 404:
            print(f"WARNING: Resource not found")
        elif e.status_code == 403:
            print(f"⚠️ WARNING: Access denied")
            print("   Solution: Ensure you have appropriate permissions")
        else:
            print(f"⚠️ WARNING: Fabric API error")
        print(f"   Status Code: {e.status_code}")
        print(f"   Details: {str(e)}")
        print(f"❌ Exception while executing fabric_rti_delete_connection: {e}")
        raise
    except Exception as e:
        print(f"WARNING: Unexpected error during connection deletion: {str(e)}")
        print(f"❌ Exception while executing fabric_rti_delete_connection: {e}")
        raise

def fabric_rti_delete_workspace(fabric_client: FabricApiClient, step_num: int = None, total_steps: int = None, workspace_id: str = None):
    """
    Delete a Fabric workspace by ID.
    
    Args:
        fabric_client: Authenticated FabricApiClient instance
        step_num: Optional current step number
        total_steps: Optional total number of steps
        workspace_id: ID of the workspace to delete
        
    Returns:
        Workspace ID if deletion successful, None if workspace not found
        
    Raises:
        FabricApiError: If deletion fails due to unexpected error
    """
    print_step(step_num, total_steps, "Deleting workspace", workspace_id=workspace_id)
    
    try:
        deleted_workspace_id = fabric_client.delete_workspace(workspace_id)
        if deleted_workspace_id:
            print(f"✅ Successfully completed: fabric_rti_delete_workspace (deleted: {deleted_workspace_id})")
            return deleted_workspace_id
        else:
            print(f"Workspace {workspace_id} was not found")
            return None
    except FabricApiError as e:
        print(f"❌ Exception while executing fabric_rti_delete_workspace: {e}")
        raise
    except Exception as e:
        print(f"❌ Exception while executing fabric_rti_delete_workspace: {e}")
        raise