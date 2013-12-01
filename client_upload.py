# coding: utf-8

__author__ = 'taciogt'


TRACKER_IP = None
TRACKER_PORT = None

MY_IP = None
UPLOADER_PORT_NUMBER = 50011


def register_as_owner_request(file_name, part_completed):

    request_data = {'method': 'REGISTER_AS_OWNER',
                    'type': 'REQUEST',
                    'file': file_name,
                    'part_number': part_completed,
                    'IP': MY_IP,
                    'port_number': UPLOADER_PORT_NUMBER
                    }

    return request_data


def _read_file_part(file_name, part_number):

        file_name = 'files/' + file_name
        f = open(file_name, 'r')
        f.seek(0, 2)
        size = f.tell()
        part_size = size / 3

        begin = part_number * part_size

        f.seek(begin)
        if part_number != 2:
            file_piece = f.read(part_size)
        else:
            file_piece = f.read(size - begin)

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


def method_router(data):
    method = data['method']

    print 'method router'
    print data

    if method == 'PING':
        ping_response()
    if method == 'DOWNLOAD_FILE':
        download_file_response()
