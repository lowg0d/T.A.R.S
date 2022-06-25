import os
import src.utils.managers.cc as cc
import src.utils.managers.conn as conn
import src.utils.managers.logs as logs
import src.addons as addons
from src import __version__

"""
T.A.R.S for ksp - by lowg0d
"""

###########################################

#launcher star function
def init():
    os.system("cls") # clear terminal
    cc.startupmessage() # send the startup message
    
    addons.load_addon("config", "src.utils.managers") # setup config manager
    conn.new_conn.first_time_conn() # connect to the game server
    
    addons.load_missions() # load missions
    #import missions.test.test as test
    #test.mission_init()
    addons.load_managers() # load managers
    addons.load_modules() # load modules
    
    # load MENU
    logs.out("loading menu...")
    import src.utils.modules.menu as menu
    logs.out("menu sucesfully loaded")
    
    # start menu
    #menu.start()
    
    import missions.test.test as test
    test.mission_init()
    
    
###########################################
    
if __name__ == '__main__':
    init()