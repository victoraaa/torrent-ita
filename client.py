# Echo server program
import socket

HOST = '192.168.0.27'                 # Symbolic name meaning all available interfaces
MAIN_PORT = 50006              # Arbitrary non-privileged port


def stub_response(host, data):
    print host, data
    return "{} is the response".format(data)


def main():
    #server shouldo do:
    #listen(MAIN_PORT, stub_response)

    #client should do:
    while True:
       data = raw_input()
       print send(HOST, MAIN_PORT, data)
    # pass

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
        response = callback(addr[0], data)
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

    print 'antes'

    #gets response
    response = s.recv(1024)
    s.close()

    print 'blah depois'
    return response


main()