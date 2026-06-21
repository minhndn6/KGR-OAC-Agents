# Catalog schema — 5 YAML lõi (đọc/sửa đúng cấu trúc)

Tất cả ở `C:\Project\KGR-OAC-Agents\OAC-Knowledge\`. Mỗi file có `_meta` ở đầu.

## workbook_catalog.yaml
```
workbooks:
  "(KGR) DB01.Revenue_v1.1":
    slug, n_datasources, n_datasources_used
    datasources: [{name, owner, used}]          # used=false → đính kèm nhưng không dùng
    canvases: [{canvas, view, n_viz,
      vizzes: [{view, chart_type(pluginType), title,
        fields: [{field, column_id, expression, sources:["<dataset>.<col>"]}] }] }]
```

## dataset_catalog.yaml
```
datasets:
  "<dataset name>":
    name, display_name, owner, description
    type: dataflow_output | db_dataset | file_upload | unknown
    produced_by_dataflows: [<flow>]             # null nếu không do dataflow sinh
    used_by_workbooks: [<title>]
    used_by_dataflows: [<flow>]
    in_closure: bool                            # có nuôi 1 trong 4 workbook không
    physical_tables: {DW_NS_*: [cols]}          # nếu đọc thẳng bảng vật lý
    file_or_other_sources: {name:[cols]}        # nguồn không phải DW (file/dim)
    columns_used_by_workbooks: [col]
    data_last_modified, folder_path
```

## dataflow_catalog.yaml
```
dataflows:
  "<flow name>":
    dataflow_id, name, object_path, last_modified, version
    input_datasets: [<name>], output_datasets: [<name>]
    in_closure: bool, n_steps
    steps: [ {step, type, ...} ]                # theo type:
      InputDataset: {input_dataset, dataset_type, physical_tables:{TBL:[cols]}}
      Join:        {join_type, left, right, on:["L = R"], condition}
      GroupBy:     {group_by:[], aggregations:["as = fn(col)"]}
      AddColumns:  {adds:[{name, expression}]}   # expression = logic nghiệp vụ
      Filter:      {filters:["expr"]}
      Concatenate: {union_type, left, right, match}
      SelectColumns/RenameColumns/OutputDataset: ...
```

## physical_table_catalog.yaml
```
physical_tables:
  DW_NS_*:
    extracted_live, verified_live(true|via_dataflow_def), base_table?
    columns_in_use:[], n_columns_in_use
    used_by_datasets:[], used_by_dataflows:[]
    nsaw_claude_ref:{table, documented_in_nsaw(bool), ref, freshness}
```

## lineage_graph.yaml
```
terminal_physical_nodes: ["physical:DW_NS_*"]
edges: [{from, to}]   # node = "workbook:<slug>/<columnID>" | "dataset:<name>[/<col>]" | "dataflow:<name>" | "physical:<TBL>"
```
Hướng edges: workbook→dataset, dataset→dataflow(producer), dataflow→dataset(input), dataset→physical. Đi xuôi = về nguồn; đi ngược = impact.

## Khóa tham chiếu (cách nối file)
- workbook field `sources` "ds.col" → key trong `dataset_catalog.datasets`.
- dataset `produced_by_dataflows` → key trong `dataflow_catalog.dataflows`.
- dataset `physical_tables` key / dataflow step `physical_tables` key → key trong `physical_table_catalog.physical_tables`.
