# -*- coding: utf-8 -*-
import dataiku
import openpyxl



DUMMY_CONSTANT = "foo"

# Init project_var to value
def set_project_var (project_var, value):
    client = dataiku.api_client()
    project_api = client.get_default_project()
    v = project_api.get_variables()
    v["standard"][project_var] = value
    project_api.set_variables(v)

# Increment project_var by inc
def inc_project_var(project_var, inc = 1):
    client = dataiku.api_client()
    project_api = client.get_default_project()
    v = project_api.get_variables()
    v["standard"][project_var] = v["standard"][project_var] + inc
    project_api.set_variables(v)

def write_wb_to_managed_folder(managed_folder_handle, wb, file_path):
    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        output = tmp.read()
        with managed_folder_handle.get_writer(file_path + ".xlsx") as w:
            w.write(output)

def write_df_in_wb(df):
    rows = dataframe_to_rows(df, index=False)
    wb = openpyxl.Workbook()
    ws = wb.active
    for r_idx, row in enumerate(rows, 1):
        for c_idx, value in enumerate(row, 1):
             ws.cell(row=r_idx, column=c_idx, value=value)
    return wb

def write_csv_to_managed_folder (managed_folder_handle, df, file_path):
    with managed_folder_handle.get_writer(file_path +".csv") as writer:
        writer.write(df.to_csv().encode("utf-8"))