import os
import src.utils.managers.cc as cc
import src.utils.managers.config as config
import src.utils.managers.mission as msn
import src.utils.managers.logs as logs
import src.addons as addons
from src import machine_name
from rich.console import Console
from rich.panel import Panel
from rich import print
from rich import box

###########################################

flight_path = "missions"
cons = Console()
console_user = f'{config.get("console_user")}@{machine_name}'
options = """
[[bold blue]1[/bold blue]] - [bold blue]Flight[/bold blue]
[[bold blue]2[/bold blue]] - [bold blue]Reload properties[/bold blue]
[[bold blue]3[/bold blue]] - [bold blue]Exit[/bold blue]
"""
panel1 = Panel(options, title="[bold blue][ Principal Menu ]", box=box.HORIZONTALS, style="bold purple3")

###########################################

def start():
    menu()

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def bonus():
    pass

def startm(path):
    Continue = True
    while Continue:
        new_mission=msn.mission(path)
        new_mission.start_flight(path)
        Continue = False
    menu()

def menu():
    os.system("cls")
    cc.systemmessage()
    follow = True
    cons.print(panel1)
    while follow:
        cmd = input(f'(menu){machine_name}$ ')
        if int(cmd) == 1:
            os.system("cls")
            cc.systemmessage()
            select_msn()
            
        elif int(cmd) == 2:
            addons.full_reload()
            
        elif int(cmd) == 3:
            print("[red]bye bye")
            exit()
        
        elif int(cmd) == 4:
            bonus()
            
        else:
            print(f'[red]"{cmd}" is not a valid option[/red]')
            pass

def select_msn():
    folder = ""
    path = ""
    message = "\n"
    counter = 0
    fl = dict()
    avaible_flights = os.listdir(f"{flight_path}")
    Continue = True
    Confirm = True

    for i in avaible_flights:
        counter += 1
        path = i
        fl[counter] = i

        try:
            mission_name = config.get_mission_config(f"{i}", "name")
            if (counter % 2) == 0: 
                message += f'[dim][[bold violet]{counter}[/bold violet]] - [bold violet]{mission_name}[/bold violet][/dim]\n'
            else:
                message += f'[[bold violet]{counter}[/bold violet]] - [bold violet]{mission_name}[/bold violet]\n'
        except:
            logs.out("mission configuraton file not found!", "error")
            
        logs.out_silence(f"flight founded: {mission_name}")

    go_back = counter + 1 
    message += f'\n[[bold violet]{go_back}[/bold violet]] - [bold violet]Go Back[/bold violet]\n'
    panel2 = Panel(message, title="[bold violet][ Select FLight ]", box=box.HORIZONTALS, style="bold yellow")
    cons.print(panel2)
    
    while Continue:
        cmd = input(f'(menu){machine_name}$ ')
        
        if has_numbers(cmd) == True:
            if cmd == go_back:
                Continue = False
                Confirm = False
                menu()
                break
            
            elif cmd in fl.keys():
                for number, path in fl.items():
                    if cmd == number:
                                path = path
                                Confirm = True
                                Continue = False
                                break
            else:
                print(f'[red]"{cmd}" is not a valid option[/red]')
        else:
            print(f'[red]"{cmd}" is not a valid option[/red]')
        
        mission_name = config.get_mission_config(f"{path}", "name")
        logs.out(f"[dim]'{mission_name}'[/dim] flight plan selected")

        logs.out(f"[bold][bold magenta]CONFIRM AND START '[dim]{mission_name.upper()}[/dim]' ? (Y/n)")
        while Confirm:
            cmd = input(f'(menu){machine_name}$ ')
            
            if cmd.upper == "Y":
                logs.out(f'starting mission: {path}')
                Continue = False
                startm(path)
                Confirm = False
                
            elif cmd.upper == "N":
                logs.out(f'starting mission: {path}')
                Continue = True
                Confirm = False
                
                
            elif cmd == "":
                logs.out(f'starting mission: {path}')
                Continue = False
                startm(path)
                Confirm = False
                
            else:
                print(f'[red]"{cmd}" is not a valid option[/red]')
                pass
            
    
