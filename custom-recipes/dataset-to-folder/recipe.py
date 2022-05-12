# Code for custom code recipe dataset-to-folder (imported from a Python recipe)

# To finish creating your custom recipe from your original PySpark recipe, you need to:
#  - Declare the input and output roles in recipe.json
#  - Replace the dataset names by roles access in your code
#  - Declare, if any, the params of your custom recipe in recipe.json
#  - Replace the hardcoded params values by acccess to the configuration map

# See sample code below for how to do that.
# The code of your original recipe is included afterwards for convenience.
# Please also see the "recipe.json" file for more information.

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# To  retrieve the datasets of an input role named 'input_A' as an array of dataset names:
input_A_names = get_input_names_for_role('input_A_role')
# The dataset objects themselves can then be created like this:
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

# For outputs, the process is the same:
output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]


# The configuration consists of the parameters set up by the user in the recipe Settings tab.

# Parameters must be added to the recipe.json file so that DSS can prompt the user for values in
# the Settings tab of the recipe. The field "params" holds a list of all the params for wich the
# user will be prompted for values.

# The configuration is simply a map of parameters, and retrieving the value of one of them is simply:
my_variable = get_recipe_config()['parameter_name']

# For optional parameters, you should provide a default value in case the parameter is not present:
my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from tempfile import NamedTemporaryFile

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# INPUT Parameters
# Input Dataset
output_dataset = dataiku.Dataset("output_iterative_1")
output_dataset_df = output_dataset.get_dataframe()

# Output Folder
output_folder = dataiku.Folder("XYRf8fQ9")

# Input dynamic name
v = dataiku.get_custom_variables()
file_name = v["iterative_step_output_prefix"] + "_" + v["iterative_step"] + ".xlsx"

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def write_wb_to_managed_folder(wb,output_folder, file_name):
    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        output = tmp.read()
        with output_folder.get_writer(file_name) as w:
            w.write(output)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def write_df_in_wb(output_dataset_df):
    rows = dataframe_to_rows(output_dataset_df, index=False)
    wb = openpyxl.Workbook()
    ws = wb.active
    for r_idx, row in enumerate(rows, 1):
        for c_idx, value in enumerate(row, 1):
             ws.cell(row=r_idx, column=c_idx, value=value)
    return wb

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
wb = write_df_in_wb(output_dataset_df)
write_wb_to_managed_folder(wb,output_folder, file_name)