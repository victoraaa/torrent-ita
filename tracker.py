import socket
import time
import json
import thread

from threading import Thread


class File(object):
    def __init__(self, name, md5):
        self.name = name
        self.providers = {}
        self.md5 = md5

    def register_provider(self, pieces, addr):
        for piece in pieces:
            if piece not in self.providers:
                self.providers[piece] = []
            if addr not in self.providers[piece]:
                self.providers[piece].append(addr)

    def remove_provider(self, addr):
        for piece, providers in self.providers.items():
            if addr in providers:
                self.providers[piece].remove(addr)

    def get_providers(self):
        response = []
        for providers in self.providers.values():
            response.append([{'IP': addr[0], 'port_number': addr[1]} for addr in providers])
        return response

    def get_json(self):
        return {'file': self.name, 'pieces_list': self.get_providers(), 'MD5': self.md5}


class Tracker(object):
    def __init__(self, port=34000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', port))

        self.commands = {
            'REGISTER_AS_OWNER': self.register,
            'LIST_FILES': self.list_files,
            'GET_TRACKER': self.get_tracker,
        }
        self.files = dict()

        t = Thread(target=self.check_providers)
        t.start()

    def loop(self):
        self.socket.listen(5)
        print '* Listening'
        while True:
            try:
                conn, addr = self.socket.accept()
                print '* New connection: {}'.format(addr[0])
                thread.start_new_thread(self.client, (conn, addr))
            except KeyboardInterrupt:
                print '* Exiting'
                self.socket.close()

    def check_providers(self):
        while False:
            providers = []
            for f in self.files:
                providers.extend(f.providers.values())
            providers = set(providers)

            for provider in providers:
                thread.start_new_thread(self.send_ping, (provider))

            time.sleep(2*60)

    def send_ping(self, addr):
        conn = socket.create_connect(addr)
        conn.sendall(json.dumps({'method': 'PING', 'type': 'REQUEST'}))
        print '-> PING: {}'.format(addr[0])
        response = conn.recv(1024)
        if response:
            response = json.loads(response)
            if response['method'] == 'PING' and response['type'] == 'RESPONSE':
                return
        for f in self.files:
            f.remove_provider(addr)

    def client(self, conn, addr):
        data = conn.recv(1024)
        if data:
            print '<- {}: {}'.format(addr[0], data)
            data = json.loads(data)
            func = self.commands[data['method']]
            response = func(data) or dict()
            response.update({'method': data['method'], 'type': 'RESPONSE'})
            print response
            print '-> {}: {}'.format(addr[0], json.dumps(response))
            conn.sendall(json.dumps(response))
            conn.close()

    def register(self, data):
        name = data['file']
        if name not in self.files:
            self.files[name] = File(name, data['MD5'])
        self.files[name].register_provider(data['part_number'], (data['IP'], data['port_number']))

    def list_files(self, data):
        return dict(files=self.files.keys())

    def get_tracker(self, data):
        if not data['file'] in self.files.keys():
            return {'error': 'FILE_NOT_AVAILABLE'}
        return self.files[data['file']].get_json()

if __name__ == '__main__':
    tracker = Tracker()
    tracker.loop()
