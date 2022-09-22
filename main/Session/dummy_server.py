import time
import socket
import threading

class Dummy_Server():

    address_family = socket.AF_INET  # IPv4
    socket_type = socket.SOCK_STREAM  # TCP
    format = "utf-8"

    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.start_listening()
        self.run_flag=True

    def get_current_time(self):
        return time.ctime(time.time())

    def start_listening(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print("Server is listening....")

    def accept_connection(self):
        self.conn, self.addr = self.socket.accept()
        print("Connected client: {}".format(self.addr))

    def close_connection(self):
        self.connected = False
        self.conn.close()

    def send_server_message(self, msg):
        msg_txt="{}\t{}".format(self.get_current_time(),msg)
        self.conn.send(msg_txt.encode(self.format))

    def send_message(self, message):
        #self.socket.send(message)
        print("The following message sent to client: {}".format(message))

    def handle(self):
        self.connected=True
        while self.connected:
            msg=self.conn.recv(1024)
            self.conn.send(msg)
            print(msg)
            #msg.split()[0]
            #self.send_message(msg)
        self.conn.close()



if __name__ == '__main__':
    host = "127.0.0.1" # localhost
    port = 1062 #The port used by the server
    server=Dummy_Server(host, port)
    while True:
        server.accept_connection()

        thread = threading.Thread(target=server.handle)
        thread.start()

    server.close_connection()


