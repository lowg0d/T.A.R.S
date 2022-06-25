import os
import time
import threading
import src.utils.managers.conn as conn
import src.utils.managers.config as config
import src.utils.managers.cc as cc
import src.utils.modules.modes as setmode
import src.utils.modules.modules as mdls
import src.utils.managers.logs as logs
import src.utils.managers.telemetry as tele

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich import box

countup_count = 0

##################################################################################

path = "test"
cons = Console()

mission_name = config.get_mission_config(path, "name")
mission_type = config.get_mission_config(path, "type")

conn = conn.new_conn.connection
ksc = conn.space_center

##################################################################################

vessel = ksc.active_vessel
vessel_name = vessel.name

print_vessel_name = f"[underline]{vessel_name}[/underline]"
config_countdown = config.get_mission_config(path, "countdown")
override_countdown = config.get_mission_config(path, "avoid_countdown")
countdown_trhottle_up = config.get_mission_config(path, "trhottle_up")
trhottle_start = config.get_mission_config(path, "trhottle_start")
target_apoapsis = config.get_mission_config(path, "target_apoapsis")
island_heading = config.get_mission_config(path, "island_heading")

vc = vessel.control
vo = vessel.orbit
ap = vessel.auto_pilot
flight = vessel.flight()

##################################################################################

def countup():
    global my_timer
    Continue = True
    
    my_timer = 0
    
    while Continue:
        my_timer =+ 1
        time.sleep(1)    
        print(f"t+ {my_timer}", end='\r')

def mission_init():
    os.system("cls")
    cc.systemmessage()
    
    #setmode.secure_mode(True)
    
    time.sleep(0.3)
    os.system("cls")
    cc.systemmessage()
    
    message = f"[bold][orange3]MISSION: [/bold][dim]{mission_name}[/dim]\n[bold][orange3]FLIGHT_TYPE: [/bold][dim]{mission_type}[/dim][/orange3]\n[bold][orange3]VESSEL: [/bold][dim]{vessel_name}[/dim][/orange3][/orange3]"
    panel2 = Panel(message, title="[green][ Flight Information ]", style="green3", title_align="left")
    panel1 = Panel(panel2, title="[bold blue][ Flight Mission Dashboard ]", box=box.HORIZONTALS, style="bold purple3")
    cons.print(panel1)

    execute_launch()

##################################################################################

def execute_launch():
    logs.out("flight information sucesfully loaded")
    time.sleep(0.1)
    logs.out("[green3]READY[/green3] - waiting for manual confirmation in secure mode")
    time.sleep(0.2)
    
    # enable ground mode
    setmode.ground_mode(True)
    
    # flight checks
    logs.out("starting pre-flight checks")
    
    # import telemetry class
    logs.out("loading vehicle telemetry")
    
    # set telemetetry
    tele.set_up_telemetry()
    
    time.sleep(0.2)
    logs.out("vehcile telemetry loaded")
    logs.out(f"establishing utilities")
    
    # get flight params
    logs.out(f"getting flight parameters")
    # give the information 
    logs.out(f"flight target review")
    logs.out(f"target ap: [dim]{target_apoapsis}m")
    logs.out(f"target Heading: [dim]{island_heading}º")
    time.sleep(0.1)
    logs.out(f"system review")
    
    mdls.override_input(True)
    mdls.autopilot(True)
    mdls.sas(True)
    mdls.rcs(True)
    
    logs.out(f"Countdown Override: [dim]{override_countdown}", prefix=print_vessel_name)
    

    
    # PRE LAUNCH
    logs.out("vehicle checks completed - ALL OK", prefix="mission control")
    # STARTUP 
    setmode.pre_flight_mode(True)
    logs.out("STARTUP STARTED", prefix="mission control")
    time.sleep(0.1)
    logs.out(f"GO FOR LAUNCH", prefix=print_vessel_name)
    logs.out(f"GO FOR LAUNCH", prefix="mission control")
    time.sleep(1)
    
    flight()

##################################################################################

def flight():
    count = 0
    mdls.countdown(int(config_countdown), int(countdown_trhottle_up), override_countdown, trhottle_start)

    ###################################################
    # go to altitude
    mdls.go_to_altitude_slow(target_apoapsis, trhottle_start, 40)

    logs.out("starting static")
    # stay static
    while int(count) < 5:
        time.sleep(0.01)
        count = count + 0.01
        print(f"t+ {int(count)}", end="\r")
        mdls.stay_static_pid()
    
    while tele.altitude_() > 5:
        if tele.v_speed_() > 10:
            mdls.set_throttle(50)        

        elif tele.v_speed_() < 10:
            mdls.set_throttle(100)

    mdls.set_throttle(0)        
    logs.out(f"Landed", prefix=print_vessel_name)
    
##################################################################################

"""
def xd():
    import utils.telemetry_manager as tele
    out(f"inicialicating flight: [dim]{mission_name}")
    ###################################################
    #utilities
    # utils
    vc = vessel.control
    vo = vessel.orbit
    ap = vessel.auto_pilot
    tlm = vessel.flight()
    
    out(f"getting flight parameters")
    with cons.status("[bold green]loading flight parameters...") as status:
        target_apoapsis = config.get_mission_config(path, "target_apoapsis")
        countdown_ss = config.get_mission_config(path, "countdown")
        island_heading = config.get_mission_config(path, "island_heading")
        #x = threading.Thread(target=countdown(10), args=(1,))
    
    out(f"target ap: [dim]{target_apoapsis}m")
    out(f"target Heading: [dim]{island_heading}º")
    time.sleep(0.2)
    
    out(f"starting flight checks")

    ap.engage()
    out(f"AutoPilot: [dim]Activated", prefix=print_vessel_name)
    time.sleep(0.2)
    
    #vc.sas = False
    out(f"SAS mode: [dim]False", prefix=print_vessel_name)
    time.sleep(0.2)
    
    vc.rcs = True
    out(f"RCS mode: [dim]True", prefix=print_vessel_name)
    time.sleep(0.2)
    
    #vc.input_mode.override
    out(f"Input Mode: [dim]Override", prefix=print_vessel_name)
    time.sleep(0.2)
    

    ###################################################
    # Pre Launch
    out("pre launch checks completed")
    out(f"[bold][bold green][underline]{vessel.name.upper()}[/underline][/bold green] IS READY FOR LAUNCH")
    
    if config.get_mission_config(path, "avoid_countdown") == True:
        out(f"[bold][orange3]AUTOMATIC AVOID COUNTDOWN [/bold][dim][red](experimental only)")
        
    elif config.get_mission_config(path, "avoid_countdown") == False:
        out(f"[bold][blink][orange3]Click Enter To Start StartUp Sequence[bold]")
        input("")
    
    out(f"StartUp Sequence Starting", prefix=print_vessel_name)
    time.sleep(0.2)
    out(f"transfering countdown control to aboard computer", prefix=print_vessel_name)
    out(f"starting countdown", prefix=print_vessel_name)
    out(f"heading rocket to flight trajectory", prefix=print_vessel_name)
    time.sleep(0.1)    
    out(f"Starting Launch Countdown", prefix=print_vessel_name)
    
    out("[blink][orange3]t- 10", prefix=("countdown"))
    time.sleep(1)
    out("[blink][orange3]t- 9", prefix=("countdown"))
    time.sleep(1)
    out("[blink][orange3]t- 8", prefix=("countdown"))
    time.sleep(1)
    out("[blink][orange3]t- 7", prefix=("countdown"))
    time.sleep(1)
    out("[blink][orange3]t- 6", prefix=("countdown"))
    time.sleep(1)
    out("[blink][orange3]t- 5", prefix=("countdown"))
    time.sleep(1)
    out("[blink][orange3]t- 4", prefix=("countdown"))
    time.sleep(1)
    out("[blink][orange3]t- 3", prefix=("countdown"))
    
    
    #x.start()
    vessel.control.lights = True
    time.sleep(0.1)
    out(f"setting throttle to: [dim]52%", prefix=print_vessel_name)
    
    vc.throttle = 0.52   
    
    time.sleep(0.9)
    out("[blink][orange3]t- 2", prefix=("countdown"))
    
    time.sleep(1)
    out("[blink][orange3]t- 1", prefix=("countdown"))
    time.sleep(1)
    
    out(f"starting engine", prefix=print_vessel_name)
    vessel.control.lights = False
    out(f"liftoff", prefix=print_vessel_name)
    vc.activate_next_stage()

    
    ############################################################################
    
    while int(tele.altitude()) <= (int(target_apoapsis/100)*10):
        pass
    out('retaying landing gear')
    vessel.control.gear = False
        
    
    while int(tele.altitude()) <= target_apoapsis:
        print(f"[blue]Ascent Phase [/blue][grey30]| [/grey30][bold cyan][dim]a:[/dim] {str(int(tele.altitude()))}[dim]m [/dim][/bold cyan][grey30]|[/grey30][bold cyan] [dim]s:[/dim] {str(int(tele.speed()))}[dim]m/s[/dim][bold cyan]", end='\r')
        ap.target_pitch_and_heading(90, 90)

    out(f"[dim]{target_apoapsis}m[/dim] apoapsis reached", prefix=print_vessel_name)

    out(f"setting throttle to: [dim]0%", prefix=print_vessel_name)
    vc.throttle = 0.2  
    
    out(f"Autopilot mode: [dim]Desactivated", prefix=print_vessel_name)
    ap.disengage()
    out(f"SAS Mode: [dim]Activated", prefix=print_vessel_name)
    ap.sas = True
    time.sleep(1)
    out(f"SAS Direction: [dim]Anti-Radial", prefix=print_vessel_name)
    ap.sas_mode = ap.sas_mode.radial
    
    while int(tele.altitude()) <= int(target_apoapsis)+(int(target_apoapsis/100)*20):
        #print(f"[blue]Ascent Phase [/blue][grey30]| [/grey30][bold cyan][dim]a:[/dim] {str(int(tele.altitude()))}[dim]m [/dim][/bold cyan][grey30]|[/grey30][bold cyan] [dim]s:[/dim] {str(int(tele.speed()))}[dim]m/s[/dim][bold cyan]", end='\r')
        ap.target_pitch_and_heading(90, 0)
    vc.throttle = 0.1 
    
    while utils.telemetry_manager.v_speed() > 8:
        pass
    
    out(f"Static Mode: [dim]Activated", prefix=print_vessel_name)
    while utils.telemetry_manager.h_speed() > 6 or utils.telemetry_manager.h_speed() < 0:       
        while utils.telemetry_manager.v_speed() > 0: 
            if utils.telemetry_manager.v_speed() < 0:            
                vc.throttle = 0.55
            elif utils.telemetry_manager.v_speed() > 0:           
                vc.throttle = 0.4
                
        while utils.telemetry_manager.v_speed() < 0:
            if utils.telemetry_manager.v_speed() > 0:
                vc.throttle = 0.4
            elif utils.telemetry_manager.v_speed() < 0:

                vc.throttle = 0.55
    
    out(f"Moving forward: [dim]10", prefix=print_vessel_name)
    while utils.telemetry_manager.h_speed() < 6:     
        vc.right = -10  
        while utils.telemetry_manager.v_speed() > 0: 
            if utils.telemetry_manager.v_speed() < 0:            
                vc.throttle = 0.55
            elif utils.telemetry_manager.v_speed() > 0:           
                vc.throttle = 0.4
                
        while utils.telemetry_manager.v_speed() < 0:
            if utils.telemetry_manager.v_speed() > 0:
                vc.throttle = 0.4
            elif utils.telemetry_manager.v_speed() < 0:

                vc.throttle = 0.55

    out(f"Moving forward: [dim]Completed", prefix=print_vessel_name)
    out(f"Moving backward: [dim]10", prefix=print_vessel_name)
    while utils.telemetry_manager.h_speed() > 2: 
        vc.right = 10
        while utils.telemetry_manager.v_speed() > 0: 
            if utils.telemetry_manager.v_speed() < 0:            
                vc.throttle = 0.55
            elif utils.telemetry_manager.v_speed() > 0:           
                vc.throttle = 0.4
            elif utils.telemetry_manager.v_speed() > 2:
                vc.throttle = 0.35
                
        while utils.telemetry_manager.v_speed() < 0:
            if utils.telemetry_manager.v_speed() > 0:
                vc.throttle = 0.4
            elif utils.telemetry_manager.v_speed() < 0:
                vc.throttle = 0.55
            elif utils.telemetry_manager.v_speed() < 2:
                vc.throttle = 0.35
    
    vc.right = 0
    out(f"Moving bakward: [dim]Completed", prefix=print_vessel_name)
    out(f"setting throttle to: [dim]25%", prefix=print_vessel_name)
    vc.throttle = 0.25
    
    out(f"STAND BY: engine start moment", prefix=print_vessel_name)
    while utils.telemetry_manager.altitude() > 15:
            if utils.telemetry_manager.v_speed() < 10:
                vc.throttle = 0.4
                
                    
            elif utils.telemetry_manager.v_speed() > 10:
                vc.throttle = 0.17
                
    
    out(f"starting landing maniover", prefix=print_vessel_name)
    while utils.telemetry_manager.altitude() > 8:
            if utils.telemetry_manager.v_speed() > 3:
                vc.throttle = 0.25                
                  
            vc.throttle = 0.35

    while utils.telemetry_manager.altitude() > 4.2:
            if utils.telemetry_manager.v_speed() > 3:
                vc.throttle = 0.8                
                  
            vc.throttle = 0.1
            
    out(f"Landed", prefix=print_vessel_name)
    
    vc.throttle = 0
    vessel.control.lights = True
"""