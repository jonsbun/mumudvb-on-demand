#!/usr/bin/python
import socket
import subprocess
from time import sleep
import psutil

HOST = ""
PORT = 4028
MUMUDVB_SCRIPT_LOCATION = "/usr/bin/mumudvb1.sh"
pid = -1
service_name = ""
timer = 5

def check_port_state():
    global listen_on_port
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        print("Currently is listening on " + str(PORT) + " port for incoming connection")
        s.listen(1)
        listen_on_port = True
    except:
        get_service_name()
        listen_on_port = False           
        
def get_service_name():
    global pid
    global service_name
    pid = get_service_pid()
    proc = psutil.Process(pid)
    service_name = proc.name()
    print("Service " + service_name + " is currectly use " + str(PORT) + " port")
            
def get_service_pid():
    while True:
        connections = psutil.net_connections()
        for c in connections:
            service_port = c.laddr[1]
            if service_port == PORT:
                return c.pid
            
def check_service_activity():
    global pid
    global timer
    global listen_on_port
    proc = psutil.Process(pid)
    conn = proc.connections()
    
    connection_status = []
    for c in conn:
        connection_status.append(c.status)
        
    if "ESTABLISHED" in connection_status:
        timer = 5
        print("Service in use. Leaving active connection")
        return
    elif timer > 0:
        print("Service is not in use. PID " + str(pid) + " will be killed after " + str(timer) + " minutes...")
        timer -= 1
    else:
        print("Killing " + service_name + " service. It was not used last 5 minutes.")
        proc.kill()
        timer = 5
        listen_on_port = True
            
if __name__ == "__main__":
    check_port_state()
    while True:
        if listen_on_port == True:
            try: 
                s.accept()
            except:
                check_port_state()
                s.accept()
            print("Received request to release port " + str(PORT))
            s.close()
            subprocess.call(MUMUDVB_SCRIPT_LOCATION)
            pid = get_service_pid()
            listen_on_port = False
        else:
            while listen_on_port == False:
                check_port_state()
                check_service_activity()
                sleep(60)
