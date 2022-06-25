import krpc
import src.utils.managers.config as config
import src.utils.managers.logs as logs
from src import __version__
from src import machine_name

global new_conn

###########################################

class Connection:
    def __init__(self, fisrt_time=False):
        self.first_time = fisrt_time # if is the first time connection
        self.connection = None # connection instance
        self.conn_name = None # connection name instance
        self.conn_addr = None # connection address instance
        self.conn_rcp_port = None # connection rcp port instance
        self.conn_stream_port = None # connection stream port instance
        self.addr_plus_port = None # address and port string to print instance

    def setup(self):
        self.conn_name = f'{machine_name}' # connection name
        self.conn_addr = config.get("conn_addr") # connection address
        self.conn_rcp_port = config.get("conn_rcp_port") # connection rcp port
        self.conn_stream_port = config.get("conn_stream_port") # connection stream port
        self.addr_plus_port = f"[{self.conn_addr}:{self.conn_rcp_port}]" # address and port string to print 
    
    def connect(self):
        ksc_conn = krpc.connect(
            name=self.conn_name,
            address=self.conn_addr,
            rpc_port=self.conn_rcp_port, stream_port=self.conn_stream_port)

        self.connection = ksc_conn
        return ksc_conn
    
    def first_time_conn(self):
        follow = True        
        while follow:
            logs.out(f"attempting connection to: [dim]{self.addr_plus_port}[/dim]")
            try:
                self.connect()
                follow = False
            except:
                logs.out(f"an error occurred while trying to connect to: [dim]{self.addr_plus_port}[/dim]", "error")
                logs.out("try again ? (y/n)")
                try_again = input("> ")
                if try_again.lower() == "y":
                    pass
                elif try_again.lower() == "":
                    pass
                elif try_again.lower() == "n":
                    follow = False
                    exit(1)
                else:
                    pass
                
        logs.out(f"sucesfully connected to:[dim]{self.addr_plus_port}[/dim]")
        logs.out(f"server version: [dim]{self.connection.krpc.get_status().version}[/dim]")
        

###########################################

new_conn = Connection()
new_conn.setup()
