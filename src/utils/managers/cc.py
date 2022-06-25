from rich import print
from src import __version__

###########################################

def systemmessage():
    message = f"""
    [bright_red]$$$$$$$$\      $$$$$$\      $$$$$$$\       $$$$$$\ [/bright_red]
    [red]\__$$  __|    $$  __$$\     $$  __$$\     $$  __$$\ [/red]
    [yellow]   $$ |       $$ /  $$ |    $$ |  $$ |    $$ /  \__| [/yellow] 
    [green]   $$ |       $$$$$$$$ |    $$$$$$$  |    \$$$$$$\ [/green]
    [blue]   $$ |       $$  __$$ |    $$  __$$<      \____$$\ [/blue]
    [cyan]   $$ |       $$ |  $$ |    $$ |  $$ |    $$\   $$ |[/cyan]
    [bright_magenta]   $$ |   $$\ $$ |  $$ |$$\ $$ |  $$ |$$\ \$$$$$$  |[/bright_magenta]
    [medium_purple]   \__|   \__|\__|  \__|\__|\__|  \__|\__| \______/[/medium_purple]     
    """                     
    print(message)

def startupmessage():
    message = f"""
    [white]» version: [dim] {__version__}[/dim]
    [white1]© 2022-present lowg0d - [dim]MIT license[/dim] 
    """           
    systemmessage()          
    print(message)

