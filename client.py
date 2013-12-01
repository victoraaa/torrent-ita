# Echo server program
import threading
import socket
import json

HOST = ''                 # Symbolic name meaning all available interfaces
MAIN_PORT = 50006              # Arbitrary non-privileged port


def stub_response(host, data):
    print host, data
    return "{} is the response".format(data)


def main():
    #server shouldo do:
    #listen(MAIN_PORT, stub_response)

    #client should do:
    ping_request('192.168.0.200', 50010)
    #while True:
        #data = raw_input()
        #print send('192.168.0.200', MAIN_PORT, data)
    pass

def ping_request(host, port):
    data = {
        "method": "PING",
        "type": "REQUEST"
    }
    try:
        response = send(host, port, json.dumps(data))
        if response["method"] == "PING" and response["type"] == "RESPONSE":
            return True
    except:
        return False


#Receives host and port to which will connect
def listen(port, callback):
    
    #initiating socket and making it listen
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        
        #transfering data
        data = conn.recv(1024)
        response = callback(addr[0], json.loads(data))
        if response:
            conn.sendall(response)
    
        conn.close()
    s.close()


#
def send(host, port, data):

    #initializing socket and making it connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    s.sendall(data)

    #gets response
    response = s.recv(1024)
    s.close()

    return response


main()