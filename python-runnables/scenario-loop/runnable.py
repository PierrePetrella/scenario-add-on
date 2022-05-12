# This file is the actual code for the Python runnable scenario-loop
import dataiku
from dataiku.runnables import Runnable


# Init project_var to value
def set_project_var (project_var, value):
    client = dataiku.api_client()
    project_api = client.get_default_project()
    v = project_api.get_variables()
    v["standard"][project_var] = value
    project_api.set_variables(v)

# Inc project_var by 1
def inc_project_var(project_var, inc = 1):
    client = dataiku.api_client()
    project_api = client.get_default_project()
    v = project_api.get_variables()
    v["standard"][project_var] = v["standard"][project_var] + inc
    project_api.set_variables(v)

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
        #Input Params
        N_input = config.get("N", None)
        if (is_int(N_input)):
            self.N= int(N_input)
        else:
            raise Exception("N must be an Integer not : " + N_input)
            
        
        self.N=config.get("N", None)
        self.scenario_name = config.get("N",None)
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None
    
    # Init project_var to value
    
    def run(self, progress_callback):
        # scenario_loop !
        iterative_step = "iterative_step"
        client = dataiku.api_client()
        project_api = client.get_default_project()
        scenario = project_api.get_scenario(self.scenario_name)

        set_project_var(iterative_step, 0)
        for i in range(self.N):
            inc_project_var(iterative_step)
            scenario.run_and_wait()
        
        