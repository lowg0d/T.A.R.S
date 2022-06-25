import time
import src.utils.managers.logs as l
import src.utils.managers.telemetry as tele
from rich import print

vessel_name = tele.vessel.name
print_vessel_name = f"[underline]{vessel_name}[/underline]"

vc = tele.vessel.control
ap = tele.vessel.auto_pilot

########### UTIL MODULES ###########

def set_throttle(inputt, silence=False):
    if silence == False:
        l.out(f"engine throttle: {str(inputt)}%", prefix=print_vessel_name)
    else:
        l.out_silence(f"engine throttle: {str(inputt)}%", prefix=print_vessel_name)
        
    N = int(inputt)/100
    vc.throttle = N
    
def pass_stage():
    l.out(f"activating next stage", prefix=print_vessel_name)
    vc.activate_next_stage()

def countdown(t, throttle_up, override, throttle_number):
    import src.utils.modules.modes as setmode
    
    l.out_silence(f"countdown: {t}s", prefix="countdown")
    temp = t*10 
    
    if override == False: 
        while temp:
            mins, secs = divmod(temp, 10)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            
            if mins > throttle_up:
                print(f"[bold magenta]t- {timer}", end="\r")
                
            elif mins == throttle_up:
                print(f"[orange3]t- {timer}", end="\r")
                sas_mode("radial")
                set_throttle(throttle_number)
                break 
            else:
                print(f"[bold magenta]t- {timer}", end="\r")
            time.sleep(0.1)
            temp -= 1
            
        while temp:
            mins, secs = divmod(temp, 10)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            
            if mins > throttle_up:
                print(f"[bold magenta]t- {timer}", end="\r")
            
            else:
                print(f"[bold magenta]t- {timer}", end="\r")
            
            time.sleep(0.1)
            temp -= 1            

    elif override == True: 
        l.out(f"[bold][orange3]AUTOMATIC AVOID COUNTDOWN [/bold][dim][red](experimental only)")  
    setmode.flight_mode(True)
    pass_stage()
    l.out("t -0", prefix="countdown")
    l.out(f"LIFTOFF CONFIRM", prefix=print_vessel_name)

def countup():
    count = 1
    while count > 0:
        count += 1
        time.sleep(1)
        return count

def get_color(percent):
    if percent >= 76:
        color = "bright_green"
    elif percent >= 51 and percent < 76:
        color = "bright_yellow"
    elif percent >= 26 and percent < 51:
        color = "light_salmon3"
    elif percent >= 1 and percent < 26:
        color = "bright_red"
        
    return color

def get_can_trasmit_science(boolean):
    if boolean == True:
        message = "True"
    if boolean == False:
        message = "[bright_red]False[/bright_red]"
    return message

def lights(boolean):
    if boolean == True:
        l.out(f"lights [dim]Activated", prefix=print_vessel_name)
        vc.lights = True
    elif boolean == False:
        l.out(f"lights [dim][red]Desactivated", prefix=print_vessel_name)
        vc.lights = False
      
def activate_action_group(group):
        l.out_silence(f"activating action group [dim]{str(group)}", prefix=print_vessel_name)
        vc.toggle_action_group(group)

def override_input(boolean):
    if boolean == True:
        l.out(f"override input [dim]Activated", prefix=print_vessel_name)
        vc.input_mode.override
    elif boolean == False:
        l.out(f"override input [red][dim]Desactivated", prefix=print_vessel_name)
        vc.input_mode.additive

def sas(boolean):
    ap.disengage()
    if boolean == True:
        l.out(f"SAS [dim]Activated", prefix=print_vessel_name)
        ap.sas = True
    elif boolean == False:
        l.out(f"SAS [dim][red]Desactivated", prefix=print_vessel_name)
        ap.sas = False

def autopilot(boolean):
    ap.disengage()
    if boolean == True:
        ap.engage()
    elif boolean == False:
        ap.disengage()

def sas_mode(mode):
    l.out(f"SAS mode: [dim]{mode}", prefix=print_vessel_name)
    ap.sas = True
    x = exec(f"ap.sas_mode = ap.sas_mode.{mode}")
    x

def rcs(boolean):
    
    if boolean == True:
        l.out(f"RCS [dim]Activated", prefix=print_vessel_name)
        vc.rcs = True
    elif boolean == False:
        l.out(f"RCS [dim][red]Desactivated", prefix=print_vessel_name)
        vc.rcs = False
        
########### FLIGHT MODULES ###########

def go_to_altitude_slow(target_altitude, throttle, final_throttle=0):
    altitde_percent = abs(target_altitude * 80 / 100)

    l.out(f"waiting to [dim]{target_altitude}m[/dim] altitude", prefix=print_vessel_name)
    
    
    while int(tele.altitude_()) < target_altitude:
        if int(tele.altitude_()) < altitde_percent:
            pass
                
        while int(tele.altitude_()) > altitde_percent and int(tele.altitude_()) < target_altitude:
                for throttle_percent in range(throttle, final_throttle, -1):
                    set_throttle(throttle_percent, True)
                    time.sleep(0.00001)     
     
    l.out(f"[dim]{target_altitude}m[/dim] altitude reached", prefix=print_vessel_name)
     
def stay_static_pid(vel=0, Continue=True):
    kp = 20
    ki = 0.35
    kd = 200
    
    error_plus = 0
    before_error = 0
    
    if int(tele.v_speed_()) < vel:
        if tele.v_speed_() != vel:
            error = tele.v_speed_()
            error_plus = error_plus + error
            
            correction_p = kp * error
            correction_i = ki * error_plus
            correction_d = kd * (error - before_error)
            
            correction_pid = (correction_p + correction_i + correction_d) * -1  
            
            set_throttle(correction_pid,
                        True)
            
            before_error = error
    
    elif int(tele.v_speed_()) > 3 and int(tele.v_speed_()) < 5:
        set_throttle(30, True)
        
    else:
        set_throttle(20, True)
            
    
def land_pid(vel=0):
    kp = 30
    ki = 0.0001
    kd = 1000
    
    suma_errores = 0
    error_anterior = 0
    if int(tele.v_speed_()) < -5:
        while tele.v_speed_() != -5:
            error = tele.v_speed_()
            suma_errores = suma_errores + error
            
            correccion_i = ki * suma_errores
            correccion_p = kp * error
            correccion_d = kd * (error - error_anterior)
            
            correccion = (correccion_p + correccion_i + correccion_d) * -1  
            
            set_throttle(correccion, True)
            error_anterior = error
            
    elif int(tele.v_speed_()) > 5:
        set_throttle(50, True)

                    
