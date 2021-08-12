import struct
import socket
import threading
import select

class client:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening = False
    queue = []

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def startListen(self):
        self.listening = True
        x = threading.Thread(target=self.__listen)
        x.start()

    def __listen(self):
        while True:
            print(self.queue)
            self.queue.append(self.decode_packet())
        
    def connect(self, password):
        self.s.connect((self.ip, self.port))
        self.send(3, password)
        
    def send(self, type, body):
        self.s.send(self.build_packet(type, body))
        if(not self.listening):
            return(self.decode_packet())

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