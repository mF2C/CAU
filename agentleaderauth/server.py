from threading import Thread
from colors import Bcolors
import socket
import ssl
from _ssl import PROTOCOL_TLS, PROTOCOL_TLSv1_2, CERT_REQUIRED
import client as caClient


class Server:
    def __init__(self, **kwargs):
        self._cert = kwargs.get("cert", None)
        self._ca = kwargs.get("ca", None)
        self._ip = kwargs.get("ip", '0.0.0.0')
        self._port = kwargs.get("port", 46400)
        self._client_s = kwargs.get("client_s", None)
        self._control = kwargs.get("control", False)
        self.__dict__.update(kwargs)
        self.server = None
        self.server_process = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.setblocking(True)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sslSocket = ssl.wrap_socket(self.sock, ssl_version=PROTOCOL_TLSv1_2, keyfile='server.key',
                                         ca_certs='it2trustedca.pem', certfile='server.pem',
                                         server_side=True)

    def start(self):
        print(Bcolors.OKGREENH + "CAU Started" + Bcolors.ENDCH)
        print(Bcolors.OKGREENH + str(self._control) + " SERVER started binding on ip: " + self._ip + " port: " + str(self._port) + Bcolors.ENDCH)
        self.sslSocket.bind((self._ip, self._port))
        print(Bcolors.OKGREENH + str(self._control) + " SERVER listening" + Bcolors.ENDCH)
        self.sslSocket.listen(50)
        global leaderH
        leaderH = None
        while True:
            client, address = self.sslSocket.accept()
            self.debug('Accepted connection from {}:{}'.format(address[0], address[1]))
            if self._control:
                leaderH = self.LeaderHandler(client=client, address=address)
                leader_handler_thread = Thread(target=leaderH.l_client_handler, args=(),
                                                         daemon=True)
                leader_handler_thread.start()
            else:
                client_handler_thread = Thread(target=self._client_handler, args=(client, address, leaderH,),
                                                         daemon=True)
                client_handler_thread.start()

    def _client_handler(self, client, address, leader):
        while True:
            payload = client.recv(65536).decode('utf-8')
            self.debug('Received payload[{}] from {}:{}'.format(payload, address[0], address[1]))
            csr = self.obtainCsr(payload)
            if csr is not None and csr != "":
                cert = caClient.Client().request(csr)
                self.debug('send back cert to client')
                if cert is not None and cert != "":
                    client.send(cert)
                    leader.send(self.obtainParameters(payload))
                    client.close()
                    return 0
            else:
                self.debug('empty csr')
                client.close()
                return 0

    class LeaderHandler:
        def __init__(self, **kwargs):
            self.client = kwargs.get('client', None)
            self.address = kwargs.get('address', None)

        def l_client_handler(self):
            self.debug('Connection from leader established')
            while True:
                payload = self.client.recv(65536).decode('utf-8')
                self.debug('Control Received payload[{}] from {}:{}'.format(payload, self.address[0], self.address[1]))
                self.client.send("control test message".encode())

        def send(self, msg):
            self.client.send(msg.encode())

        def debug(self, text):
            print(Bcolors.FAILH + " Control SERVER " + text + Bcolors.ENDCH)

    def obtainCsr(self, request):
        tmp = request.rsplit(',', 8)[0]
        return tmp[4:]

    def obtainParameters(self, request):
        tmp = request.split(',')[1] + ',' + request.split(',')[2] + ',' + \
              request.split(',')[3] + ',' + request.split(',')[4]
        return tmp

    def debug(self, text):
        print(Bcolors.FAILH + str(self._control) + " SERVER " + text + Bcolors.ENDCH)


if __name__ == "__main__":
    server = Server(port=46400, control=False)
    server_process = Thread(target=server.start, args=(), daemon=True)

    serverC = Server(port=46401, control=True)
    server_processC = Thread(target=serverC.start, args=(), daemon=True)

    server_process.start()
    server_processC.start()

    server_process.join()
    server_processC.join()
