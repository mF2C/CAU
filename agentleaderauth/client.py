import httplib2
import os


class Client:

    def __init__(self, **kwargs):
        self._cert = kwargs.get("cert", None)
        self._key = kwargs.get("key", None)
        self._ca = kwargs.get("ca", None)
        self.__dict__.update(kwargs)

    def request(self, csr):
        return self._connect_(csr)

    def _connect_(self, csr):
        cacert = os.path.join(os.path.dirname(os.path.abspath("it2untrustedca.pem")), "it2untrustedca.pem")
        client_cert = open("server.pem")
        client_key = open("server.key")
        self._ca_domain = "https://213.205.14.13:54443/certauths/rest/uc2untrustedca"
        # create the client
        self._https = httplib2.Http(disable_ssl_certificate_validation=True)
        self._https.ca_certs = cacert
        self._https.add_certificate(client_key, client_cert, self._ca_domain)
        response, content = self._https.request(self._ca_domain,
                                                'POST', headers={'content-type': 'text/plain', 'accept': 'text/plain'},
                                                body=csr)
        print("Response from CA: " + str(response) + " || content: " + content.decode())
        return str(content).encode('utf-8')

    @staticmethod
    def debug(text):
        print("CLIENT " + text)


if __name__ == '__main__':
    csr = ca_cert = open("testR.csr")
    Client().request(csr)
