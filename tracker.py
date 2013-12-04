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
        self.port = port
        self.commands = {
            'REGISTER_AS_OWNER': self.register,
            'LIST_FILES': self.list_files,
            'GET_TRACKER': self.get_tracker,
        }
        self.files = dict()

    def loop(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.port))
        s.listen(5)
        print '* Listening'
        while True:
            try:
                conn, addr = s.accept()
                print '* New connection: {}'.format(addr[0])
                # Nova conexão -> cria uma nova thread para ela, que roda self.client
                thread.start_new_thread(self.client, (conn, addr))
            except KeyboardInterrupt:
                print '* Exiting'
                s.close()

    def client(self, conn, addr):
        # Thread que lida com as requisições de clientes
        data = conn.recv(1024)
        if data:
            print '<- {}: {}'.format(addr[0], data)
            data = json.loads(data)
            func = self.commands[data['method']]
            response = func(data) or dict()  # Resposta computada a ser enviada ao cliente
            response.update({'method': data['method'], 'type': 'RESPONSE'})
            print '-> {}: {}'.format(addr[0], json.dumps(response))
            conn.sendall(json.dumps(response))
            conn.close()

    def register(self, data):
        # Registrar um cliente como provider de uma parte de um arquivo
        name = data['file']
        if name not in self.files:
            self.files[name] = File(name, data['MD5'])
        self.files[name].register_provider(data['part_number'], (data['IP'], data['port_number']))

    def list_files(self, data):
        # Recuperar os arquivos que já foram registrados
        return dict(files=self.files.keys())

    def get_tracker(self, data):
        # Recuperar a lista de providers de um arquivo
        if not data['file'] in self.files.keys():
            return {'error': 'FILE_NOT_AVAILABLE'}
        return self.files[data['file']].get_json()

if __name__ == '__main__':
    tracker = Tracker()
    tracker.loop()
