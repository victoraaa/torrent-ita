# coding: utf-8

__author__ = 'victoraaa'

from client import send

TRACKER = ''
TRACKER_PORT = 500001


def main_test():
    download_file_part('192.168.0.26', 50011, 'test_file.txt', 0)


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
        t = threading.Thread(target=download_file_part, args = (host, port, filename, part))
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
    with open(filename, 'wb') as f:
        f.write("".join(parts))
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

main_test()