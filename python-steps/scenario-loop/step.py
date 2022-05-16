# This file is the code for the plugin Python step scenario-loop

import os, json
from dataiku.customstep import *

# the plugin's resource folder path (string)
resource_folder = get_step_resource()

# settings at the plugin level (set by plugin administrators in the Plugins section)
plugin_config = get_plugin_config()

# settings at the step instance level (set by the user creating a scenario step)
step_config = get_step_config()
