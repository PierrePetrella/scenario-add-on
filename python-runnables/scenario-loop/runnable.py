# This file is the actual code for the Python runnable scenario-loop
import dataiku
from dataiku.runnables import Runnable
from io_utils import *



class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.step_project_var = "step"
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
        ### Get and Check Input Params 
        
        self.scenario_name = config.get("scenario",None)
        
   
        loop_type = config.get("loop_type", None)
        self.loop_list = []
        if (loop_type == "counter"):
            N_input = config.get("N", None)
            if (str.isdigit(N_input)):
                self.N= int(N_input)
                self.loop_list = range(self.N)
            else:
                raise Exception("N must be an Integer not : " + N_input)
        
        elif (loop_type == "column_values"):
            dataset_name = config.get("dataset", None)
            loop_dataset = dataiku.Dataset(dataset_name)
            column_name = config.get("column_name", None)
            df = loop_dataset.get_dataframe()
            if column_name in df:
                self.loop_list = list(df[column_name])
            else:
                raise Exception (column_name + " is not in " + dataset_name)
        
        else:
            raise Exception (loop_type + " loop_type is not supported")


    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None
    
    # Init project_var to value
    def run(self, progress_callback):
        # scenario_loop !
        
        client = dataiku.api_client()
        project_api = client.get_default_project()
        scenario = project_api.get_scenario(self.scenario_name)

        
        for step in self.loop_list:
            set_project_var(self.step_project_var,step)
            scenario.run_and_wait()
        
        