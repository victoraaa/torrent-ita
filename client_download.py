# coding: utf-8

__author__ = 'victoraaa'

import threading
import os
import logging

from client import send, N_PARTS

logging.level(logging.INFO)

TRACKER = '127.0.0.1'
TRACKER_PORT = 34000


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
        logging.info('Response received: ' + str(response))
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
    print 
