import time
import src.utils.managers.logs as logs
import src.utils.managers.conn as conn
import src.utils.modules.modules as mdls

###########################################

conn = conn.new_conn.connection
ksc = conn.space_center
vessel = ksc.active_vessel
current_flight = vessel.flight()
refframe = vessel.orbit.body.reference_frame
ap = vessel.auto_pilot

###########################################

altitude_ = conn.add_stream(getattr, current_flight, 'surface_altitude')
apoapsis_altitude_ = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis_altitude_ = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
surface_altitude_ = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')

speed_ = conn.add_stream(getattr,vessel.flight(refframe), 'speed')
v_speed_ = conn.add_stream(getattr,vessel.flight(refframe), 'vertical_speed')
h_speed_ = conn.add_stream(getattr,vessel.flight(refframe), 'horizontal_speed')

position_ = conn.add_stream(vessel.position,refframe)
latitude_ = conn.add_stream(getattr, current_flight, 'latitude')
longitude_ = conn.add_stream(getattr, current_flight, 'longitude')

rotation_ = conn.add_stream(vessel.rotation,refframe)
pitch_ = conn.add_stream(getattr, current_flight, 'pitch')
heading_ = conn.add_stream(getattr, current_flight, 'heading')
roll_ = conn.add_stream(getattr, current_flight, 'roll')

direction_ = conn.add_stream(vessel.direction,refframe)
throttle_ = conn.add_stream(getattr, vessel.control, 'throttle')
available_thrust_ = conn.add_stream(getattr, vessel, "available_thrust")
max_thrust_ = conn.add_stream(getattr, vessel, "max_thrust")
thrust_ = conn.add_stream(getattr, vessel, "thrust")

right = conn.add_stream(getattr, vessel.control, 'right')
up = conn.add_stream(getattr, vessel.control, 'up')
pitch_control = conn.add_stream(getattr, vessel.control, 'pitch')
roll_control = conn.add_stream(getattr, vessel.control, 'roll')
yaw_control = conn.add_stream(getattr, vessel.control, 'yaw')
available_thrust = conn.add_stream(getattr,vessel,'available_thrust')

roll_pid = conn.add_stream(getattr, ap,'roll_pid_gains')
yaw_pid = conn.add_stream(getattr, ap,'yaw_pid_gains')
pitch_pid = conn.add_stream(getattr, ap,'pitch_pid_gains')

def set_up_telemetry():
    try:
        print_vessel_name = f"[underline]{vessel.name}[/underline]"
        signal_strength_float = vessel.comms.signal_strength
        signal_strength_decimals = "{:.2f}".format(signal_strength_float)
        signal_strength_format_percent = float(signal_strength_decimals)*100
        signal_strength_format = f"[{mdls.get_color(signal_strength_format_percent)}]{signal_strength_format_percent}%[/{mdls.get_color(signal_strength_format_percent)}]"
        can_trasmit_science = mdls.get_can_trasmit_science(vessel.comms.can_transmit_science)
        logs.out(f"signal strength: [dim]{signal_strength_format}[/dim]", prefix=print_vessel_name)
        time.sleep(0.1)
        logs.out(f"can trasmit science: [dim]{can_trasmit_science}[/dim]", prefix=print_vessel_name)
        
    except:
        logs.out("Error setting up telemetry streams", "error")