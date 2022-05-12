import dataiku
from dataiku.customrecipe import *


import pandas as pd, numpy as np
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from tempfile import NamedTemporaryFile

client = dataiku.api_client()
project = client.get_default_project()

### Get handles in INPUT and OUTPUT 
# Get handle on input dataset
input_dataset_name = get_input_names_for_role('input_dataset')[0]
input_dataset = dataiku.Dataset(input_dataset_name)
input_dataset_df = input_dataset.get_dataframe()

# Get handle on output dataset name to feed to the "COPY" query
output_folder_id = get_output_names('output_folder')[0].split(".")[1]
output_folder = dataiku.Folder(output_folder_id)


# Get handle on the PARAMS
file_path = get_recipe_config().get('file_path', None)
file_type = get_recipe_config().get('file_type', None)


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
    with managed_folder_handle.get_writer(file_path) as writer:
        writer.write(df.to_csv().encode("utf-8"))


if (file_type == "csv"):
    write_csv_to_managed_folder (output_folder, input_dataset_df, file_path)
elif (file_type == "excel"):
    wb = write_df_in_wb(input_dataset_df)
    write_wb_to_managed_folder(output_folder, wb, file_path) 
else:
    raise Exception ("Export file type : " + file_type + " is not supported")
