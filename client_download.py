# coding: utf-8

__author__ = 'victoraaa'

import threading
import os
import logging
import md5
import base64

from client import send, N_PARTS

# logging.basicConfig(filename='client_download.log', level=logging.INFO)
# logging.basicConfig(level=logging.INFO)

TRACKER = '192.168.0.10'
TRACKER_PORT = 34000

MY_IP = '192.168.0.255'
UPLOADER_PORT_NUMBER = 50000

def main_test():
    download_file('192.168.0.26', 50011, 'ring.jpg')


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
        response = send(TRACKER, TRACKER_PORT, data)
        print response
    except:
        msg = 'Tracker {}:{} is unreachable'.format(TRACKER, TRACKER_PORT)
        logging.error(msg)

def get_tracker(filename):
    data = {
        "method": "LIST_FILES",
        "type": "REQUEST",
        "file": filename
    }
    try:
        response = send(TRACKER, TRACKER_PORT, data)
    except:
        return "Tracker is unreachable"


def download_file(host, port, filename):
    #download all parts
    threads = []    
    for i in range(N_PARTS):
        t = threading.Thread(target=download_file_part, args = (host, port, filename, i))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
        #send message to tracker

    #put files together
    parts = []
    for i in range(N_PARTS):
        with open('{}.part{}'.format(filename, i), 'rb') as f:
            parts.append(f.read())
        os.remove('{}.part{}'.format(filename, i))
    with open(filename, 'wb') as f:
        f.write("".join(parts))
    #check if original
    
    return


def register_as_owner(file_name, part_completed=None):
    data = {'method': 'REGISTER_AS_OWNER',
            'type': 'REQUEST',
            'file': file_name,
            'part_number': part_completed,
            'IP': MY_IP,
            'port_number': UPLOADER_PORT_NUMBER
            }

    # registering the file when starting the client
    if part_completed is None:
        f = open(file_name)
        md5_code = md5.new(f.read()).digest()
        data['MD5'] = base64.b64encode(md5_code)
        data['part_number'] = [0, 1, 2]
    # registering the file after downloading one part
    else:
        data['part_number'] = [part_completed]

    response = send(TRACKER, TRACKER_PORT, data)
    print response
    
    logging.info('Response: {}'.format(response))


def download_file_part(host, port, filename, part):
    request = {
        "method": "DOWNLOAD_FILE",
        "type": "REQUEST",
        "file": filename,
        "part_number": part
    }
    try:
        response = send(host, port, request)
    except:
        return "host is unreachable"
    print response
    with open('{}.part{}'.format(filename, part), 'wb') as f:
        f.write(response["file"])

if __name__ == '__main__':
    list_files()

    # file_name = 'test_file.txt'
    # register_as_owner(file_name)
