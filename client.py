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


def main():
    #server shouldo do:
    #listen(MAIN_PORT)

    #client should do:
    print ping_request(HOST, 50006)
    #while True:
        #data = raw_input()
        #print send('192.168.0.200', MAIN_PORT, data)
    pass

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
        data = conn.recv(1024).decode('utf-8')

        t = threading.Thread(target=_process_connection, args = (data, conn))
        t.start()
    s.close()


def _process_connection(data, conn):
    #vê data e chama o método responsável

    response = route(json.loads(data))

    response = json.dumps(response)
    print '\nResposta a ser enviada:'
    if len(response) < 100:
        print response
    else:
        print response[0:100] + '....'

    if response:
        # import time
        # time.sleep(0.1)
        conn.sendall(response)
        # time.sleep(0.1)
    conn.close()


def route(data):
    #check data 'method' and 'type' and send to responsible method
    method = data["method"]
    method_type = data["type"]

    # status
    print '\nChamada recebida:'
    print 'METHOD: ' + method
    print 'TYPE: ' + method_type

    if method == 'DOWNLOAD_FILE' and method_type == "REQUEST":
        return download_file_response(data)
    else:
        return "Invalid Request"


def send(host, port, data):

    #initializing socket and making it connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    s.sendall(json.dumps(data))
    #gets response
    response = s.recv(1024)
    s.close()

    try:
        response = json.loads(response)
    except Exception as e:
        print e
        print response

    return response


if __name__ == '__main__':
    # main()
    listen(MAIN_PORT)