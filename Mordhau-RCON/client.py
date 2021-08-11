import struct
import socket

class client:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self, password):
        self.s.connect((self.ip, self.port))
        self.send(3, password)
        
    def send(self, type, body):
        self.s.send(self.build_packet(type, body))
        while True:
            (in_length,) = struct.unpack("<i", self.read_packet(4))
            in_payload = self.read_packet(in_length)
            return(in_payload.decode()[:-3])

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