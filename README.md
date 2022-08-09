# Scenario Loop Pluggin

![GitHub release (latest by date)](https://img.shields.io/github/v/release/dataiku/dss-plugin-) ![Build status](https://img.shields.io/badge/build-passing-brightgreen) ![Support level](https://img.shields.io/badge/support-Unsupported-orange)

This Dataiku plugin is composed of two components:
- A scenario step to loop through a scenario multiple times. 
- A visual recipe that exports a dataset to a managed folder (with dynamic naming)

Documentation https://drive.google.com/drive/folders/1sEqBQCe5ADdbqc7xHo5N_HeKzKGS-_Cp


## Loop Scenario Step:
Input parameters:
- Scenario to Loop through
- Looping method :
	- Counter : requires N (number of loops) to be defined
	- Column values : Requires a dataset and column name to loop through every value of that column,
Usage:
- Define a scenario to run one iteration of your Flow
- Then define a master scenario to loop through the "one interation" Scenario.

NOTE : To implement to concept of iterative macro (and add a stopping condition) you can:
- Define a scenario to run one iteration of your Flow
- Then define a scenario to run the "one iteration" scenario on a given condition
- Then define a master scenario to loop through the "condition scenario" Scenario N number of times.


## Dataset to Folder Recipe:
Input : DSS Dataset
Output : Managed Folder
Usage: 
- Define the type of the file export of the dataset to the Managed Folder (.csv OR .xlsx)
- Dynamically name the output file.

## License

This plugin is distributed under the [Apache License version 2.0](LICENSE).