import struct
import socket
import threading
import select
import library.mordhau_commands as mordhau_commands
import time
import config
import json

class client:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mordhau = mordhau_commands.mordhau_commands()

    listening = False
    json = False
    queue = []

    def __init__(self, shell_mode = False):
        self.ip = config.host
        self.port = config.port
        self.mordhau.socket = self
        self.shell_mode = shell_mode

    def start_listen(self, keepAlive=True):
        self.listening = True
        x, y = threading.Thread(target=self.__listen), threading.Thread(target=self.__keep_alive)
        x.start(); y.start()

    def __keep_alive(self):
        while True:
            if(not self.json):
                self.run("alive")
                time.sleep(110)

    def __listen(self):
        while True:
            if(self.shell_mode): print(self.decode_packet().strip())
            else: self.queue.append(self.decode_packet())
        
    def connect(self, use_json=False):
        self.s.connect((self.ip, self.port))
        if(not use_json):
            self.send(3, config.password)
        else:
            self.send(3, json.dumps({ "password":config.password }))
        
    def send(self, type, body):
        self.s.send(self.build_packet(type, body))
        if(not self.listening):
            return(self.decode_packet())

    def run(self, body):
        return self.send(2, body)

    def decode_packet(self):
        in_data = ""
        while True:
            (in_length,) = struct.unpack("<i", self.read_packet(4))
            in_payload = self.read_packet(in_length)
            in_data_partial, in_padding = in_payload[8:-2], in_payload[-2:]
            in_data += in_data_partial.decode("utf8")
            if len(select.select([self.s], [], [], 0)[0]) == 0:
                return in_data

    def read_packet(self, length):
        data = b""
        while len(data) < length:
            data += self.s.recv(length - len(data))
        return data

    def build_packet(self, type, body):
        terminator = b'\x00\x00'
        payload = (
            struct.pack("<ii", 0, type) + body.encode("utf8") + terminator
        )
        length = struct.pack("<i", len(payload))
        return(length + payload)