#coding: utf-8
# Echo server program
import threading
import socket
import json

from client_upload import download_file_response

#HOST = '192.168.0.27'                 # Symbolic name meaning all available interfaces
HOST = ''
MAIN_PORT = 50000         # Arbitrary non-privileged port

TRACKER = ''
TRACKER_PORT = 500001

N_PARTS = 3


#Waits for connections and starts new threads for each incoming connection
def listen(port):
    #Creates a new socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Makes the socket be reusable so that if the connections have problems,
    #we can still listen at the same port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    #Makes the socket listen
    s.listen(5)
    #waits for connections, accepts them, receives the data, and starts a new thread for the connection
    while True:
        conn, addr = s.accept()

        #transfering data
        data = conn.recv(1024).decode('utf-8')

        t = threading.Thread(target=_process_connection, args = (data, conn))
        t.start()
    s.close()


def _process_connection(data, conn):
    #gets the response from the responsible to answer the request
    response = route(json.loads(data))
    #if there's a response, we answer it
    if response:
        conn.sendall(json.dumps(response))
        import time
        time.sleep(0.1)

    #after answering the request, we close the connection
    conn.close()


#Gets a request and sends it to the function responsible to processing it
def route(data):
    #check data 'method' and 'type' and send to responsible method
    method = data["method"]
    method_type = data["type"]

    #logs the request
    print '\nChamada recebida:'
    print 'METHOD: ' + method
    print 'TYPE: ' + method_type
    print 'FULL REQUEST:' + data

    #makes the routing based on 'method' and 'method_type'
    if method == 'DOWNLOAD_FILE' and method_type == "REQUEST":
        return download_file_response(data)
    else:
        return "Invalid Request"


#sends a message to a machine and returns the response
def send(host, port, data):

    #initializing socket and making it connect to the host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    s.sendall(json.dumps(data))

    #wait a bit for the connection to be ok
    import time
    time.sleep(0.01)

    #gets response
    response = ""
    while True:
        _buffer = s.recv(1024**2)
        if _buffer:
            response += _buffer
        else:
            break
    
    time.sleep(0.1)
    s.close()
    #we transform the JSON in an object
    return json.loads(response)


if __name__ == '__main__':
    # main()
    listen(MAIN_PORT)
