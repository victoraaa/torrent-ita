#coding: utf-8
# Echo server program
import threading
import socket
import json

from client_upload import download_file_response

#HOST = '192.168.0.27'                 # Symbolic name meaning all available interfaces
HOST = ''
MAIN_PORT = 50006              # Arbitrary non-privileged port

TRACKER = ''
TRACKER_PORT = 500001

N_PARTS = 3


def main():
    #server shouldo do:
    #listen(MAIN_PORT)

    #client should do:
    print ping_request(HOST, 50006)
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


def list_files():
    data = {
        "method": "LIST_FILES",
        "type": "REQUEST"
    }
    try:
        pass
    except:
        pass


def download_file(host, port, filename):
    threads = []    
    for i in range(N_PARTS):
        t = threading.Thread(target=download_file_part, args = (host, port, filename, part))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
        #send message to tracker
    #put files together
    #check if original
    
    return


def download_file_part(host, port, filename, part):
    request = {
        "method": "DOWNLOAD_FILE",
        "type": "request",
        "file": filename,
        "part_number": part
    }
    response = send(host, port, request)
    with open('filename.part1', 'wb') as f:
        f.write(response)


#Receives host and port to which will connect

def listen(port):    
    #initiating socket and making it listen
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    while True:
        conn, addr = s.accept()

        #transfering data
        data = conn.recv(1024)

        t = threading.Thread(target=_process_connection, args = (data, conn))
        t.start()
    s.close()

def _process_connection(data, conn):
    #vê data e chama o método responsável

    response = route(json.loads(data))
    if response:
        conn.sendall(json.dumps(response))
    conn.close()

def route(data):
    #check data 'method' and 'type' and send to responsible method
    method = response["method"]
    method_type = response["type"]

    if method == "PING" and method_type == "RESPONSE":
        return ping_reply(data)
    elif method == 'DOWNLOAD_FILE' and method_type == "RESPONSE":
        return download_file_response(data)


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
