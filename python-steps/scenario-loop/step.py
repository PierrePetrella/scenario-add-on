# This file is the code for the plugin Python step scenario-loop

import os, json
from dataiku.customstep import *
from io_utils import *


# INITIALISATION 
step_project_var = "step"

# the plugin's resource folder path (string)
resource_folder = get_step_resource()

# settings at the plugin level (set by plugin administrators in the Plugins section)
plugin_config = get_plugin_config()

# settings at the step instance level (set by the user creating a scenario step)
step_config = get_step_config()

        
        
### Get and Check Input Params 

scenario_name = step_config.get("scenario",None)


loop_type = step_config.get("loop_type", None)
loop_list = []
if (loop_type == "counter"):
    N_input = step_config.get("N", None)
    print (str.isdigit(N_input))
    print (int(N_input))
    if (str.isdigit(N_input)):
        N= int(N_input)
        loop_list = range(N)
    else:
        raise Exception("N must be an Integer not : " + N_input)

elif (loop_type == "column_values"):
    dataset_name = step_config.get("dataset", None)
    loop_dataset = dataiku.Dataset(dataset_name)
    column_name = step_config.get("column_name", None)
    df = loop_dataset.get_dataframe()
    if column_name in df:
        loop_list = list(df[column_name])
    else:
        raise Exception (column_name + " is not in " + dataset_name)

else:
    raise Exception (loop_type + " loop_type is not supported")
    
    
### Run Loop

client = dataiku.api_client()
project_api = client.get_default_project()
scenario = project_api.get_scenario(scenario_name)


for step in loop_list:
    set_project_var(step_project_var,step)
    scenario.run_and_wait()