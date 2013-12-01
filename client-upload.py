# encoding: utf-8

__author__ = 'taciogt'

from client import listen, send
# from tracker import get_part_bytes  # pra saber o range de bytes correspondente a uma determinada parte


TRACKER_HOST = '192.168.0.27'
TRACKER_PORT = 50006


MY_IP = None
MY_PORT_NUMBER = None


def register_as_owner_request(file_name, part_completed):

    request_data = {'method': 'REGISTER_AS_OWNER',
                    'type': 'REQUEST',
                    'file': file_name,
                    'part_number': part_completed,
                    'IP': MY_IP,
                    'port_number': MY_PORT_NUMBER
                    }

    send(TRACKER_HOST, TRACKER_PORT, request_data)


def download_file_response(request_data):
    file_name = request_data['file']
    part_number = request_data['part_number']

    f = open(file_name, 'r')

    begin, end = get_part_bytes(file_name, part_number)
    part_size = end - begin
    f.seek(begin)
    file_piece = f.read(part_size)

    response_data = {'method': 'DOWNLOAD_FILE',
                     'type': 'RESPONSE',
                     'file': file_piece
                     }
    send(request_data['IP'], request_data['PORT_NUMBER'], response_data)


def ping_response():
    response_data = {'method': 'PING',
                     'type': 'RESPONSE'}

    send(TRACKER_HOST, TRACKER_PORT, response_data)


def method_router(data):
    method = data['method']

    if method == 'PING':
        ping_response()


if __name__ == "__main__":

    while True:
        listen(50010, method_router)
