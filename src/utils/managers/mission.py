import time
class mission():
    def __init__(self, name) -> None:
        self.name = name
        self.path = f"missions/{name}/"
    
    def start_flight(self, name):
        execute1 = exec(f"import missions.{name}.{name} as msn")
        execute2 = exec(f"msn.mission_init()")
        
        execute1
        time.sleep(0.1)
        execute2