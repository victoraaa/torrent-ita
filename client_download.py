# coding: utf-8

__author__ = 'victoraaa'

import threading
import os
import logging
import md5
import itertools
import base64

from client import send, N_PARTS

# logging.basicConfig(filename='client_download.log', level=logging.INFO)
# logging.basicConfig(level=logging.INFO)

TRACKER = '192.168.0.10'
TRACKER_PORT = 34000

MY_IP = '192.168.0.26'
UPLOADER_PORT_NUMBER = 50000

class InvalidFile(Exception):
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
        response = send(TRACKER, TRACKER_PORT, data)
        print response
    except:
        msg = 'Tracker {}:{} is unreachable'.format(TRACKER, TRACKER_PORT)
        logging.error(msg)

def download_file_view(filename):
    def get_hosts_combination(hosts_lists):
        host_combinations = list(itertools.product(*hosts_lists))
        n = N_PARTS
        while n > 0:
            for combination in host_combinations:
                if len(set(combination)) == n:
                    return combination
            n -= 1

        #shouldn't get here
        raise Exception("something strange happening")

    try:
        tracker = _get_tracker(filename)
    except ValueError:
        print 'The chosen file is not available. Please check your spelling.'

    hosts_lists = []
    for i in range(N_PARTS):
        hosts_lists.append([host["IP"] for host in tracker["pieces"][i]])
    hosts_by_part = get_hosts_combination(hosts_lists)

    hosts = []
    for i in range(N_PARTS):
        for host in tracker["pieces"][i]:
            if host["IP"] == hosts_by_part[i]:
                hosts.append(host)

    try:
        _download_file(hosts, filename, tracker["MD5"])
    except InvalidFile:
        print "The download file is invalid! It may be corrupted or attacked."


def _get_tracker(filename):
    data = {
        "method": "GET_TRACKER",
        "type": "REQUEST",
        "file": filename
    }
    try:
        response = send(TRACKER, TRACKER_PORT, data)
    except:
        return "Tracker is unreachable"

    if "error" in response:
        raise ValueError("File not available at tracker")

    return {
        "filename": filename,
        "MD5": base64.b64decode(response["MD5"]),
        "pieces": response["pieces_list"]
    }


def _download_file(hosts, filename, MD5):
    #download all parts
    threads = []    
    for i in range(N_PARTS):
        t = threading.Thread(target=_download_file_part, args = (hosts[i]["IP"], hosts[i]["port_number"], filename, i))
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
        f.write(base64.b64decode("".join(parts)))

    #check if original
    with open(filename, 'rb') as f:
        hashed_file = md5.new(f.read())
        if hashed_file.digest() != MD5:
            raise InvalidFile("the hash of the download file is not valid")


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
        f = open('files/' + file_name)
        md5_code = md5.new(f.read()).digest()
        data['MD5'] = base64.b64encode(md5_code)
        data['part_number'] = [0, 1, 2]
    # registering the file after downloading one part
    else:
        data['part_number'] = [part_completed]

    response = send(TRACKER, TRACKER_PORT, data)
    print response

    logging.info('Response: {}'.format(response))


def _download_file_part(host, port, filename, part):
    request = {
        "method": "DOWNLOAD_FILE",
        "type": "REQUEST",
        "file": filename,
        "part_number": part
    }
    try:
        response = send(host, port, request)
    except Exception as e:
        print e
        return "host is unreachable"

    with open('{}.part{}'.format(filename, part), 'wb') as f:
        f.write(response["file"])

    register_as_owner(filename, part_completed=part)


if __name__ == '__main__':
    list_files()

    #register_as_owner('test_file.txt')
    #register_as_owner('ring.jpg')

    #list_files()
    #_get_tracker("test_file.txt")
    #download_file_view("ring.jpg")
    #download_file_view("test_file.txt")
