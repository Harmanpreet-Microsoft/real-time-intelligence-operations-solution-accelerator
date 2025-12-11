# GET DATA SOURCE SCHEMA

## url

Schema:
GET `https://{hostname}/webapi/capacities/{capacity_id}/workloads/ML/AISkill/Automatic/v1/workspaces/{workspace_id}/artifacts/{artifact_id}}/schema?responseSource=live&dataSourceType=kusto`

'webapi/capacities/ab4dc2db-09b5-4547-8045-e329fcb5ad77/workloads/ML/AISkill/Automatic/v1/workspaces/4a51ee0e-5cc8-4f29-8e3e-9d154c72ddfc/artifacts/d4565878-aa04-4fb1-8b57-6bbbe92fc0b3/schema?responseSource=live&dataSourceType=kusto'


Example:
GET `https://ab4dc2db09b545478045e329fcb5ad77.pbidedicated.windows.net/webapi/capacities/ab4dc2db-09b5-4547-8045-e329fcb5ad77/workloads/ML/AISkill/Automatic/v1/workspaces/4a51ee0e-5cc8-4f29-8e3e-9d154c72ddfc/artifacts/d4565878-aa04-4fb1-8b57-6bbbe92fc0b3/schema?responseSource=live&dataSourceType=kusto`

## headers

Schema:
```
Content-Type: application/json
x-ms-upstream-artifact-id: {data_agent_id}
x-ms-workload-resource-moniker: {str(uuid.uuid4())}
```

Example:
```
Content-Type: application/json
x-ms-upstream-artifact-id: def679f2-2d5c-470d-91ba-3951748daed3
x-ms-workload-resource-moniker: 0b629f01-fd8d-4727-b93a-940eba9f40d1
```

## Schema content


```json
{
  "cacheLastUpdatedTime": "2025-12-11T10:50:47.0635791+00:00",
  "schema": {
    "type": "kusto",
    "database_name": "rti_kqldb_rtisaaghtblp2",
    "workspace_id": "4a51ee0e-5cc8-4f29-8e3e-9d154c72ddfc",
    "kusto_id": "d4565878-aa04-4fb1-8b57-6bbbe92fc0b3",
    "endpoint": "https://trd-cshzstwk8f66ujg11x.z0.kusto.fabric.microsoft.com",
    "id": "d4565878-aa04-4fb1-8b57-6bbbe92fc0b3",
    "display_name": "rti_kqldb_rtisaaghtblp2",
    "user_description": null,
    "additional_instructions": null,
    "metadata": {},
    "elements": [
      {
        "id": "04df2cb3-70aa-4e39-b4e6-a45f996036b1",
        "is_selected": false,
        "display_name": "locations",
        "type": "kusto.table",
        "description": null,
        "children": [
          {
            "id": "Id",
            "is_selected": true,
            "display_name": "Id",
            "type": "kusto.column",
            "data_type": "System.Int32",
            "description": null,
            "children": []
          },
          {
            "id": "City",
            "is_selected": true,
            "display_name": "City",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Country",
            "is_selected": true,
            "display_name": "Country",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          }
        ]
      },
      {
        "id": "047fa917-b7df-42d8-bba2-34980c209689",
        "is_selected": false,
        "display_name": "sites",
        "type": "kusto.table",
        "description": null,
        "children": [
          {
            "id": "Id",
            "is_selected": true,
            "display_name": "Id",
            "type": "kusto.column",
            "data_type": "System.Int32",
            "description": null,
            "children": []
          },
          {
            "id": "Name",
            "is_selected": true,
            "display_name": "Name",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "LocationId",
            "is_selected": true,
            "display_name": "LocationId",
            "type": "kusto.column",
            "data_type": "System.Int32",
            "description": null,
            "children": []
          },
          {
            "id": "PlantType",
            "is_selected": true,
            "display_name": "PlantType",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          }
        ]
      },
      {
        "id": "696ac71b-0dfa-4fa8-942c-3824641b461a",
        "is_selected": false,
        "display_name": "assets",
        "type": "kusto.table",
        "description": null,
        "children": [
          {
            "id": "Id",
            "is_selected": true,
            "display_name": "Id",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Name",
            "is_selected": true,
            "display_name": "Name",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "SiteId",
            "is_selected": true,
            "display_name": "SiteId",
            "type": "kusto.column",
            "data_type": "System.Int32",
            "description": null,
            "children": []
          },
          {
            "id": "Type",
            "is_selected": true,
            "display_name": "Type",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "SerialNumber",
            "is_selected": true,
            "display_name": "SerialNumber",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "MaintenanceStatus",
            "is_selected": true,
            "display_name": "MaintenanceStatus",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          }
        ]
      },
      {
        "id": "5c90801c-3bce-4602-9e4c-7b603f49ffc8",
        "is_selected": false,
        "display_name": "products",
        "type": "kusto.table",
        "description": null,
        "children": [
          {
            "id": "Id",
            "is_selected": true,
            "display_name": "Id",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "CategoryId",
            "is_selected": true,
            "display_name": "CategoryId",
            "type": "kusto.column",
            "data_type": "System.Int32",
            "description": null,
            "children": []
          },
          {
            "id": "CategoryName",
            "is_selected": true,
            "display_name": "CategoryName",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Name",
            "is_selected": true,
            "display_name": "Name",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Description",
            "is_selected": true,
            "display_name": "Description",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "BrandName",
            "is_selected": true,
            "display_name": "BrandName",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Number",
            "is_selected": true,
            "display_name": "Number",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Status",
            "is_selected": true,
            "display_name": "Status",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Color",
            "is_selected": true,
            "display_name": "Color",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "ListPrice",
            "is_selected": true,
            "display_name": "ListPrice",
            "type": "kusto.column",
            "data_type": "System.Double",
            "description": null,
            "children": []
          },
          {
            "id": "UnitCost",
            "is_selected": true,
            "display_name": "UnitCost",
            "type": "kusto.column",
            "data_type": "System.Double",
            "description": null,
            "children": []
          },
          {
            "id": "IsoCurrencyCode",
            "is_selected": true,
            "display_name": "IsoCurrencyCode",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          }
        ]
      },
      {
        "id": "e6e06ddd-6b1c-4ca8-99ec-f4e52d9e0e7b",
        "is_selected": false,
        "display_name": "events",
        "type": "kusto.table",
        "description": null,
        "children": [
          {
            "id": "Id",
            "is_selected": true,
            "display_name": "Id",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "AssetId",
            "is_selected": true,
            "display_name": "AssetId",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "ProductId",
            "is_selected": true,
            "display_name": "ProductId",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Timestamp",
            "is_selected": true,
            "display_name": "Timestamp",
            "type": "kusto.column",
            "data_type": "System.DateTime",
            "description": null,
            "children": []
          },
          {
            "id": "BatchId",
            "is_selected": true,
            "display_name": "BatchId",
            "type": "kusto.column",
            "data_type": "System.String",
            "description": null,
            "children": []
          },
          {
            "id": "Vibration",
            "is_selected": true,
            "display_name": "Vibration",
            "type": "kusto.column",
            "data_type": "System.Double",
            "description": null,
            "children": []
          },
          {
            "id": "Temperature",
            "is_selected": true,
            "display_name": "Temperature",
            "type": "kusto.column",
            "data_type": "System.Double",
            "description": null,
            "children": []
          },
          {
            "id": "Humidity",
            "is_selected": true,
            "display_name": "Humidity",
            "type": "kusto.column",
            "data_type": "System.Double",
            "description": null,
            "children": []
          },
          {
            "id": "Speed",
            "is_selected": true,
            "display_name": "Speed",
            "type": "kusto.column",
            "data_type": "System.Double",
            "description": null,
            "children": []
          },
          {
            "id": "DefectProbability",
            "is_selected": true,
            "display_name": "DefectProbability",
            "type": "kusto.column",
            "data_type": "System.Double",
            "description": null,
            "children": []
          }
        ]
      }
    ]
  }
}
```