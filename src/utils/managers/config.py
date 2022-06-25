import os
import sys
import json
import src.utils.managers.logs as logs 

"""
tars config manager
"""

###########################################
# check if config exists

if not os.path.isfile('./config/config.json'):
    logs.out("'config.json' not found! Please add it and try again.", "error")
    sys.exit()
    
else:
    with open('./config/config.json') as file:
        config_file = json.load(file)

###########################################
# get functions

def get(parameter):
    try:
        response = config_file[f'{parameter}'] # get the parameter from the config file
        return response # resturn the parameter
    except:
        logs.out('parameter not in the config.json', 'error')
        exit()

def get_subconfig(name, parameter):
    try:
        subconfig_file = subconfig_file(name) # get the config file
        response = subconfig_file[f'{parameter}'] # get the parameter from the config file
        return response # resturn the parameter
    except:
        logs.out(f'parameter not in the {name}.json', 'error')
        exit()

def get_mission_config(name, parameter):
    try:
        mission_config_file = mission_config_configfile(name) # get the config file
        response = mission_config_file[f'{parameter}'] # get the parameter from the config file
        return response # resturn the parameter
    except:
        logs.out(f'parameter not in the ./missions/{name}/mission.json', 'error')
        exit()

###########################################
# utils

def subconfig_configfile(name):
    path = f'./config/{name}.json'
    if not os.path.isfile(path):
        logs.out(f"'{name}.json' not found! Please add it and try again.", "error")
        exit("configuration file doesent exits")
        
    else:
        with open(path) as file:
           sub_config_file = json.load(file)
        return sub_config_file

def mission_config_configfile(name):    
    path = f'./missions/{name}/mission.json'
    if not os.path.isfile(path):
        logs.out(f"'mission.json' for {name} not found! Please add it and try again.", "error")
        exit("configuration file doesent exits")
    else:
        with open(f'./{path}') as file:
            mission_config_file = json.load(file)
        return mission_config_file
    
###########################################