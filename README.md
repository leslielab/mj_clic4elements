# mj_clic4elements
Python integration of clic for nikon elements.

Put this code into elements
import socket
import json

def call_server(class_name, method, *args, host= "127.0.0.1", port=65432, **kwargs):
    '''
    class_name (str): ['clic']
    method (str):  - name of the function that you want to call
    
    '''
    
    # connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # parse the command
    command = {"class": class_name,
               "method": method,
               "args": args,
               "kwargs": kwargs}
    s.send((json.dumps(command).encode()))
    
    response = s.recv(4096).decode()
    s.close()
    return json.loads(response)


# YOU NEED TO EDIT THIS.
# EACH METHOD IS CALLED BY THIS FUNCTION
#result1 = call_server("clic", "enableJoystick")
#result1 = call_server("clic", "disableJoystick")
result1 = call_server("clic", "changeVoltage", 69.420, 25)
