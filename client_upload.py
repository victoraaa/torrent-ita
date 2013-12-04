# coding: utf-8

import base64

__author__ = 'taciogt'


TRACKER_IP = None
TRACKER_PORT = None

MY_IP = None


def _read_file_part(file_name, part_number):

        file_name = 'files/' + file_name
        f = open(file_name, 'rb')
        
        f.seek(0, 2)
        size = f.tell()
        part_size = size / 3

        f.seek(0,0)
        file_content = f.read()

        file_content = base64.b64encode(file_content)
        
        size = len(file_content)
        begin = part_number * part_size

        if part_number != 2:
            file_piece = file_content[begin:begin+part_size]
        else:
            file_piece = file_content[begin:]

        return file_piece


def download_file_response(request_data):
    file_name = request_data['file']
    part_number = request_data['part_number']

    file_piece = _read_file_part(file_name, part_number)

    response_data = {'method': 'DOWNLOAD_FILE',
                     'type': 'RESPONSE',
                     'file': file_piece
                     }

    return response_data


def ping_response():
    print 'ping response'
    response_data = {'method': 'PING',
                     'type': 'RESPONSE'}

    return response_data
