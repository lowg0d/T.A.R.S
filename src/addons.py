import os
import time
from pathlib import Path
import src.utils.managers.logs as logs

################################################

missions_folder = 'missions'
managers_folder = 'src/utils/managers'
modules_folder = 'src/utils/modules'

missions_path = Path(f'./{missions_folder}')
managers_path = Path(f'./{managers_folder}')
modules_path = Path(f'./{modules_folder}')

mission_list = os.listdir(f'./{missions_folder}')
managers_list = os.listdir(f'./{managers_folder}')
module_list = os.listdir(f'./{modules_folder}')

files_in_manager_path = managers_path.iterdir()
files_in_modules_path = modules_path.iterdir()

addon_prefix = 'addons'
managers_prefix = 'managers'
mission_prefix = 'missions'
modules_prefix = 'modules'

################################################

def load_addon(name, direction="src.utils.addons"):
    logs.out(f'loading "{name}"...', prefix=addon_prefix)
    try:
        execute = exec(f'import {direction}.{name}')
        execute
        time.sleep(0.1)
    except:
        logs.out(f'error loading "{name}" addon', 'error')
        
    logs.out(f'"{name}" sucesfully loaded!', prefix=addon_prefix)
    
def load_managers():
    logs.out(f'loading managers...', prefix=managers_prefix)
    for i in files_in_manager_path:
        manager = str(i.name).replace('.py', '')
        if i.is_file():
            try:
                execute = exec(f'import src.utils.managers.{manager}')
                execute
            except:
                logs.out(f'error loading "{manager}" manager', 'error')
                exit()
                
            #logs.out(f'"{manager}" sucesfully imported!')
            
    logs.out(f'managers sucesfully loaded!', prefix=managers_prefix)

def load_missions():
    logs.out(f'loading missions...', prefix=mission_prefix)
    for mission in mission_list:
        try:
            execute = exec(f'import {missions_folder}.{mission}.{mission}')
            execute
        except:
            logs.out(f'error loading "{mission}" mission, {mission}.py not found', 'error')
            exit()
            
        #logs.out(f'"{mission}" sucesfully imported!')
        
    logs.out(f'missions sucesfully loaded!', prefix=mission_prefix)

def load_modules():
    logs.out(f'loading modules...', prefix=modules_prefix)
    for i in files_in_modules_path:
        modul = str(i.name).replace('.py', '')
        if i.is_file():
            try:
                execute = exec(f'import src.utils.modules.{modul}')
                execute
            except:
                logs.out(f'error loading "{modul}" modul', 'error')
                exit()
                
            #logs.out(f'"{modul}" sucesfully loaded!')
            
    logs.out(f'modules sucesfully loaded!', prefix=modules_prefix)

#############################################

def reload_addon(name):
    logs.out(f'reloading "{name}"...', prefix=addon_prefix)
    
    try:
        execute1 = exec(f'del {name}')
        execute2 = exec(f'import src.utils.managers.{name}')
        
        execute1
        time.sleep(0.01)
        execute2
    except:
        pass 
        logs.out(f'error loading "{name}"', 'error')
        
    logs.out(f'"{name}" sucesfully reloaded!', prefix=addon_prefix)
      
def reload_managers():
    logs.out(f'reloading managers...', prefix=managers_prefix)
    for i in files_in_manager_path:
        manager = str(i.name).replace('.py', '')
        if i.is_file():
            try:
                execute1 = exec(f'del {manager}')
                execute2 = exec(f'import src.utils.managers.{manager}')
                
                execute1
                time.sleep(0.01)
                execute2
                
            except:
                logs.out(f'error reloading "{manager}" manager', 'error')
                #exit()
            
    logs.out(f'sucesfully reloaded managers', prefix=managers_prefix)

def reload_missions():
    logs.out(f'reloading missions...', prefix=mission_prefix)
    for mission in mission_list:
        try:
            #execute1 = exec(f'del missions.{mission}.{mission}')
            execute2 = exec(f'import missions.{mission}.{mission}')

            #execute1
            time.sleep(0.01)
            execute2
            
        except:
            logs.out(f'error reloading "{mission}" mission', 'error')
            #exit()
            
    logs.out(f'sucesfully reloaded missions', prefix=mission_prefix)
  
def reload_modules():
    logs.out(f'reloading modules...', prefix=modules_prefix)
    count = 0
    for i in files_in_modules_path:
        modul = str(i.name).replace('.py', '')
        if i.is_file():
            try:
                execute1 = exec(f'del {modul}')
                execute2 = exec(f'import src.utils.modules.{modul}')
                
                execute1
                time.sleep(0.01)
                execute2
                
                count += 1
            except:
                logs.out(f'error reloading "{modul}" modules', 'error')
                #exit()
            
    logs.out(f'sucesfully reloaded modules', prefix=modules_prefix)

#############################################

def unload_addon(name, direction="src.utils.addons"):
    logs.out(f'unloading "{name}"...', prefix=addon_prefix)
    try:
        execute = exec(f'del {direction}.{name}')
        execute
        time.sleep(0.1)
    except:
        pass 
        logs.out(f'error unloading "{name}"', 'error')
    logs.out(f'"{name}" sucesfully unloaded!', prefix=addon_prefix)
    
def unload_mission(name):
    logs.out(f'unloading "{name}"...')
    try:
        execute = exec(f'del missions.{name}', prefix=mission_prefix)
        execute
        time.sleep(0.1)
    except:
        pass 
        logs.out(f'error unloading "{name}"', 'error')
    logs.out(f'"{name}" sucesfully unloaded!', prefix=mission_prefix)
    
def unload_modul(name):
    logs.out(f'unloading "{name}" module...', prefix=modules_prefix)
    try:
        execute = exec(f'del src.modules.{name}')
        execute
        time.sleep(0.1)
    except:
        pass 
        logs.out(f'error unloading "{name}" module', 'error')
    logs.out(f'"{name}" module sucesfully unloaded!', prefix=modules_prefix)
    
#############################################

def full_reload():
    reload_managers()
    time.sleep(0.1)
    reload_missions()
    time.sleep(0.1)
    reload_modules()