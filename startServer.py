from server import flaskServer
from core import case
from gevent.wsgi import WSGIServer
from core import config
import ssl
from os.path import isfile


def get_ssl_context():
    if config.https.lower() == "true":
        # Sets up HTTPS
        if config.TLS_version == "1.2":
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        elif config.TLS_version == "1.1":
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        if isfile(config.certificatePath) and isfile(config.privateKeyPath):
            context.load_cert_chain(config.certificatePath, config.privateKeyPath)
            return context
        else:
            flaskServer.displayIfFileNotFound(config.certificatePath)
            flaskServer.displayIfFileNotFound(config.privateKeyPath)
    return None


if __name__ == "__main__":
    case.initialize_case_db()
    ssl_context = get_ssl_context()
    try:
        port = int(config.port)
        if ssl_context:
            server = WSGIServer(('', 5000), application=flaskServer.app, ssl_context=ssl_context)
        else:
            server = WSGIServer(('', 5000), application=flaskServer.app)
        server.serve_forever()
    except ValueError:
        print('Invalid port {0}. Port must be an integer'.format(config.port))
