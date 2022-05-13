import dataiku
from dataiku.customrecipe import *
from io_utils import *

import pandas as pd, numpy as np
import openpyxl
from tempfile import NamedTemporaryFile

client = dataiku.api_client()
project = client.get_default_project()

def write_df_in_wb(df):
    rows = dataframe_to_rows(df, index=False)
    wb = openpyxl.Workbook()
    ws = wb.active
    for r_idx, row in enumerate(rows, 1):
        for c_idx, value in enumerate(row, 1):
             ws.cell(row=r_idx, column=c_idx, value=value)
    return wb

### Get handles in INPUT and OUTPUT 
# Get handle on input dataset
input_dataset_name = get_input_names_for_role('input_dataset')[0]
input_dataset = dataiku.Dataset(input_dataset_name)
input_dataset_df = input_dataset.get_dataframe()

# Get handle on output dataset name to feed to the "COPY" query
output_folder_id = get_output_names('output_folder')[0].split(".")[1]
output_folder = dataiku.Folder(output_folder_id)


### Get handle on the PARAMS
file_path = get_recipe_config().get('file_name', None)
file_type = get_recipe_config().get('file_type', None)


if (file_type == "csv"):
    write_csv_to_managed_folder (output_folder, input_dataset_df, file_path)
elif (file_type == "excel"):
    wb = write_df_in_wb(input_dataset_df)
    write_wb_to_managed_folder(output_folder, wb, file_path) 
else:
    raise Exception ("Export file type : " + file_type + " is not supported")
