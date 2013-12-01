# Echo server program
import threading
import socket
import json

HOST = '192.168.0.27'                 # Symbolic name meaning all available interfaces
MAIN_PORT = 50006              # Arbitrary non-privileged port

TRACKER = ''
TRACKER_PORT = 500001

def stub_response(data):
    print host, data
    return "{} is the response".format(data)


def main():
    #server shouldo do:
    #listen(MAIN_PORT, stub_response)

    #client should do:
    print ping_request('192.168.0.26', 50011)
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
        response = send(host, port, data)
        if response["method"] == "PING" and response["type"] == "RESPONSE":
            return True
    except:
        return False

def download_file(host, port, filename):
    pass

def list_files():
    data = {
        "method": "LIST_FILES",
        "type": "REQUEST"
    }
    try:
        pass
    except:
        pass

def download_file_part(host, port, filename, part):
    request = {
        "method": "DOWNLOAD_FILE",
        "type": "request",
        "file": filename,
        "part_number": part
    }
    response = send(host, port, request)
    #do whatever we do with the response


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
        response = callback(json.loads(data))
        if response:
            conn.sendall(json.dumps(response))

        conn.close()
    s.close()


#
def send(host, port, data):

    #initializing socket and making it connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    s.sendall(json.dumps(data))
    #gets response
    response = s.recv(1024)
    s.close()

    return json.loads(response)


if __name__ == '__main__':
    main()
