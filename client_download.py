# coding: utf-8

__author__ = 'victoraaa'


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

