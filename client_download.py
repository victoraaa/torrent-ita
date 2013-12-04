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

TRACKER = '127.0.0.1'
TRACKER_PORT = 34000

MY_IP = '127.0.0.1'
UPLOADER_PORT_NUMBER = 50000


#Represents an InvalidFile Exception
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


#puts together each phase of the download
def download_file_view(filename):
    #a function that returns a combinations of hosts for each part that
    #maximizes the number of hosts that we'll use for download
    def get_hosts_combination(hosts_lists):
        #creates all combinations of hosts
        host_combinations = list(itertools.product(*hosts_lists))
        n = N_PARTS
        #searches for a combination that has the maximum possible
        #number of different hosts
        while n > 0:
            for combination in host_combinations:
                if len(set(combination)) == n:
                    return combination
            n -= 1

        #shouldn't get here
        raise Exception("something strange happening")

    #gets the .tracker from the Tracker server
    try:
        tracker = _get_tracker(filename)
    except ValueError:
        print 'The chosen file is not available. Please check your spelling.'

    #for each part of the file, concatenates the hosts that have it from the .tracker info
    hosts_lists = []
    for i in range(N_PARTS):
        hosts_lists.append([host["IP"] for host in tracker["pieces"][i]])
    hosts_by_part = get_hosts_combination(hosts_lists)

    #generates a list of hosts ips and ports for each part of the file
    hosts = []
    for i in range(N_PARTS):
        for host in tracker["pieces"][i]:
            if host["IP"] == hosts_by_part[i]:
                hosts.append(host)

    #downloads the file
    try:
        _download_file(hosts, filename, tracker["MD5"])
    except InvalidFile:
        print "The download file is invalid! It may be corrupted or attacked."


#sends a message to the tracker and returns the received .tracker info
def _get_tracker(filename):
    #from the protocol
    data = {
        "method": "GET_TRACKER",
        "type": "REQUEST",
        "file": filename
    }
    #sends the request
    try:
        response = send(TRACKER, TRACKER_PORT, data)
    except:
        return "Tracker is unreachable"

    #if the tracker does not have the file, raise an Exception
    if "error" in response:
        raise ValueError("File not available at tracker")

    #returns the .tracker info
    return {
        "filename": filename,
        "MD5": base64.b64decode(response["MD5"]),
        "pieces": response["pieces_list"]
    }


#downloads the varios parts of a file, puts them together and check if it is the original file
def _download_file(hosts, filename, MD5):
    #download all parts, making a new thread for each part
    threads = []
    for i in range(N_PARTS):
        #creates a new thread that runs the _download_file_part method
        t = threading.Thread(target=_download_file_part, args = (hosts[i]["IP"], hosts[i]["port_number"], filename, i))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

    #put files together in an unique file and deletes the parts
    parts = []
    for i in range(N_PARTS):
        with open('{}.part{}'.format(filename, i), 'rb') as f:
            parts.append(f.read())
        os.remove('{}.part{}'.format(filename, i))

    #save the full file
    with open("./files/{}".format(filename), 'wb') as f:
        f.write(base64.b64decode("".join(parts)))

    #check if hash is the same as the original
    with open("./files/{}".format(filename), 'rb') as f:
        hashed_file = md5.new(f.read())
        if hashed_file.digest() != MD5:
            raise InvalidFile("the hash of the download file is not valid")

    register_as_owner(filename)


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

    logging.info('Response: {}'.format(response))


#downloads one part of the file
def _download_file_part(host, port, filename, part):
    request = {
        "method": "DOWNLOAD_FILE",
        "type": "REQUEST",
        "file": filename,
        "part_number": part
    }
    try:
        #logs the action
        print "Downloading file {} from host {}, at port {}. Request is: {}".format(
            filename, host, port, request)
        #sends the request to the host and gets the response
        response = send(host, port, request)
    except Exception as e:
        print e
        return "host is unreachable"

    #saves the file part
    with open('{}.part{}'.format(filename, part), 'wb') as f:
        f.write(response["file"])

    #sends message to the tracker saying that we've got the part we just downloaded
    register_as_owner(filename, part_completed=part)


if __name__ == '__main__':
    list_files()

    #register_as_owner('test_file.txt')
    #register_as_owner('ring.jpg')

    #list_files()
    #_get_tracker("test_file.txt")
    #download_file_view("ring.jpg")
    #download_file_view("test_file.txt")
