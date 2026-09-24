import socket 
import json

def initTCP(systems):
    # define the socket parameters
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen(5) # become a server socket, maximum 5 connections

    print(f'listening on {HOST}:{PORT}')

    systems = {"clic": CLIC_DEVICE}
    while True:
        client_socket, client_addr = serversocket.accept()
        print(f'connection from {client_addr}')

        # need to read message from the clinet
        data = client_socket.recv(4096).decode()

        if not data:
            client_socket.close()
            continue

        try:
            command = json.loads(data)
            class_name = command.get("class")
            method_name = command.get("method")
            args = command.get("args", [])
            kwargs = command.get("kwargs", [])

            #if class_name not in systems:
            if class_name not in systems:
                response = {"status": "error",
                            "message": f"No such class {class_name}"}
            
            # get the right device
            obj = systems[class_name]
            # check if method is in the device
            if hasattr(obj, method_name):
                method = getattr(obj, method_name)
                result = method(*args, **kwargs)
                response = {"status": "ok",
                            "result": result}
            # else
            else:
                response = {"status": "error",
                            "message": f"No such method {method_name}"}

        except Exception as e:
            print(e)

        client_socket.send(json.dumps(response).encode())
        client_socket.close()