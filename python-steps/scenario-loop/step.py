# This file is the code for the plugin Python step scenario-loop

import os, json
from dataiku.customstep import *
from io_utils import *


### INITIALISATION 
step_project_var = "step"
resource_folder = get_step_resource()
plugin_config = get_plugin_config()
step_config = get_step_config()
        
# Get and Check Input Params 

scenario_name = step_config.get("scenario",None)

loop_type = step_config.get("loop_type", None)
loop_list = []
if (loop_type == "counter"):
    pattern = re.compile("^(\${)+.*}")   
    if (pattern.match(N_input)):

        var_name = N_input[2:-1]
        var_value = get_project_var(var_name)

        if (var_value !=None):
            N_input = str(var_value)
        else:
            raise Exception("Project variable : {}, does not exist for this project".format(var_name))


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
    
    
### RUN LOOP

client = dataiku.api_client()
project_api = client.get_default_project()
scenario = project_api.get_scenario(scenario_name)


for step in loop_list:
    set_project_var(step_project_var,step)
    scenario.run_and_wait()