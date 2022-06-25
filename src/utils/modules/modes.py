import src.utils.managers.logs as logs
from src.utils.modules.modules import activate_action_group

code = "9"

def secure_mode(boolean):
    if boolean == True:
        logs.out("[green3]ACTIVATED", prefix=("[bold blue]SECURE MODE[/bold blue]"))
        secure_console()
        
    elif boolean == False:
        logs.out("[red]DESACTIVATED", prefix=("[bold blue]SECURE MODE[/bold blue]"))
    else:
        exit()

def ground_mode(boolean):
    if boolean == True:
        logs.out("[green3]ACTIVATED", prefix=("[violet]GROUND MODE[/violet]"))
        activate_action_group(5)
        #console("ground")
        
    elif boolean == False:
        activate_action_group(6)
        #out("[red]DESACTIVATED", prefix=("[violet]GROUND MODE[/violet]"))
    else:
        secure_mode(True)

def pre_flight_mode(boolean):
    if boolean == True:
        activate_action_group(3)
        ground_mode(False)
        logs.out("[green3]ACTIVATED", prefix=("[bold orange3]STARTUP MODE[/bold orange3]"))
    elif boolean == False:
        activate_action_group(2)
    else:
        secure_mode(True)
        
def flight_mode(boolean):
    if boolean == True:
        activate_action_group(4)
        logs.out("[green3]ACTIVATED", prefix=("[bold yellow3]FLIGHT MODE[/bold yellow3]"))
        pre_flight_mode(False)
        
    elif boolean == False:
        activate_action_group(1)
        logs.out("[red]DESACTIVATED", prefix=("[bold yellow3]FLIGHT MODE[/bold yellow3]"))
        
    else:
        secure_mode(True)

##################################################################################

def secure_console():
    confirm = True
    while confirm:
        cmd = input("(secure) low@tars_mk2# ")
        if cmd.upper() == "MODE -G":
            code_input = input("code> ")
            if code_input == code:
                secure_mode(False)
                confirm = False
            else:
                logs.out("invalid code", "error")
                pass 
            
def console(mode):
    confirm = True
    while confirm:
        cmd = input(f"({mode}) low@tars_mk2$ ")
        if cmd.upper() == "ARM":
            logs.out("starting ground checks")
            confirm = False
            pass


