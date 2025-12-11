#!/usr/bin/env python3
"""
Fabric Data Agent Setup Module

This module provides Data Agent creation functionality for Microsoft Fabric operations.
It creates a new Data Agent in the specified workspace.

Usage:
    python fabric_data_agent.py --workspace-id "workspace-guid" --data-agent-name "MyDataAgent"

Requirements:
    - fabric_api.py module in the same directory
    - Azure CLI authentication or other Azure credentials configured
    - Appropriate permissions to create Data Agents in the workspace
"""

import argparse
import sys
from typing import Optional
from fabric_api import FabricApiClient, FabricWorkspaceApiClient, FabricApiError


def create_data_agent(workspace_client: FabricWorkspaceApiClient, 
                      data_agent_name: str,
                      kusto_db_id: Optional[str] = None,
                      cluster_uri: Optional[str] = None,
                      database_name: Optional[str] = None) -> dict:
    """
    Create a Data Agent in the workspace and optionally add a Kusto database data source.
    
    Args:
        workspace_client: Authenticated FabricWorkspaceApiClient instance
        data_agent_name: Name of the Data Agent to create
        kusto_db_id: Optional ID of the Kusto database to connect as data source
        cluster_uri: Optional URI of the Kusto cluster for schema retrieval
        database_name: Optional name of the database for schema retrieval
        
    Returns:
        dict: Data Agent information if successful
        
    Raises:
        FabricApiError: If creation fails
    """
    print(f"🤖 Creating Data Agent: '{data_agent_name}'")
    
    try:
        # Check if Data Agent already exists
        existing_agent = workspace_client.get_data_agent_by_name(data_agent_name)
        if existing_agent:
            data_agent_id = existing_agent.get('id', 'N/A')
            print(f"ℹ️  Data Agent '{data_agent_name}' already exists with ID: {data_agent_id}")
            data_agent = existing_agent
        else:
            # Create the Data Agent
            data_agent = workspace_client.create_data_agent(data_agent_name)
            data_agent_id = data_agent.get('id', 'N/A')
            print(f"✅ Successfully created Data Agent: {data_agent_name} ({data_agent_id})")
        
        # If a Kusto database ID is provided, add it as a data source
        if kusto_db_id:
            print(f"🔗 Adding Kusto database '{kusto_db_id}' as data source...")
            try:
                datasource = workspace_client.create_data_agent_data_source(
                    data_agent_id=data_agent_id,
                    data_source_id=kusto_db_id,
                    data_source_type="kqldatabase"
                )
                datasource_id = datasource.get('id', 'N/A')
                print(f"✅ Successfully added data source: {kusto_db_id} ({datasource_id})")
                
                # If cluster URI and database name are provided, retrieve and display schema
                if cluster_uri and database_name:
                    print(f"📊 Retrieving schema for database '{database_name}'...")
                    try:
                        schema = workspace_client.get_kql_database_schema(
                            cluster_uri=cluster_uri,
                            database_name=database_name
                        )
                        
                        print(f"✅ Successfully retrieved schema for database '{database_name}'")
                        print(f"   Tables found: {len(schema.get('tables', {}))}")
                        
                        # Display table information
                        for table_name, table_info in schema.get('tables', {}).items():
                            column_count = len(table_info.get('columns', []))
                            print(f"   - {table_name}: {column_count} columns")
                            
                    except FabricApiError as e:
                        print(f"⚠️ Warning: Failed to retrieve schema: {e}")
                        
            except FabricApiError as e:
                print(f"⚠️ Warning: Failed to add data source '{kusto_db_id}': {e}")
                print("Data Agent was created successfully, but without the data source.")
        
        return data_agent
        
    except FabricApiError as e:
        print(f"❌ Failed to create Data Agent '{data_agent_name}': {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error creating Data Agent '{data_agent_name}': {e}")
        raise FabricApiError(f"Error creating Data Agent: {e}")


def main():
    """Main function to create a Data Agent and optionally add a data source."""
    parser = argparse.ArgumentParser(
        description="Create a Microsoft Fabric Data Agent with optional Kusto database data source",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create Data Agent only
  python fabric_data_agent.py --workspace-id "12345678-1234-1234-1234-123456789012" --data-agent-name "Operations Agent"
  
  # Create Data Agent with Kusto database data source
  python fabric_data_agent.py --workspace-id "12345678-1234-1234-1234-123456789012" --data-agent-name "Operations Agent" --kusto-db-id "87654321-4321-4321-4321-210987654321"
  
  # Create Data Agent with data source and retrieve schema
  python fabric_data_agent.py --workspace-id "12345678-1234-1234-1234-123456789012" --data-agent-name "Operations Agent" --kusto-db-id "87654321-4321-4321-4321-210987654321" --cluster-uri "https://cluster.kusto.windows.net" --database-name "manufacturing_db"
        """
    )
    
    parser.add_argument(
        "--workspace-id", 
        required=True, 
        help="ID of the workspace where the Data Agent will be created"
    )
    
    parser.add_argument(
        "--data-agent-name", 
        required=True, 
        help="Name of the Data Agent to create"
    )
    
    parser.add_argument(
        "--kusto-db-id", 
        required=False, 
        help="Optional ID of the Kusto database to add as a data source"
    )
    
    parser.add_argument(
        "--cluster-uri", 
        required=False, 
        help="Optional URI of the Kusto cluster for schema retrieval (e.g., 'https://cluster.kusto.windows.net')"
    )
    
    parser.add_argument(
        "--database-name", 
        required=False, 
        help="Optional name of the database for schema retrieval"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create workspace client
    try:
        workspace_client = FabricWorkspaceApiClient(workspace_id=args.workspace_id)
        
        # Create the Data Agent with optional data source
        result = create_data_agent(
            workspace_client=workspace_client,
            data_agent_name=args.data_agent_name,
            kusto_db_id=args.kusto_db_id,
            cluster_uri=args.cluster_uri,
            database_name=args.database_name
        )
        
        print(f"\n✅ Data Agent ID: {result.get('id', 'N/A')}")
        print(f"✅ Data Agent Name: {args.data_agent_name}")
        if args.kusto_db_id:
            print(f"✅ Kusto Database ID: {args.kusto_db_id}")
        
    except FabricApiError as e:
        print(f"❌ Fabric API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()