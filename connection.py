import socket

IP = "192.168.0.2"
PORT = 12289
class Connection:# Modified the function above to class
    def __init__(self, ip="192.168.0.2", port=12289, timeout=5.0):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.ip, self.port))
        print(f"✓ Connected to {self.ip}:{self.port}")

    def query(self, command: str):
        """Send an ASCII command, return response as bytes"""
        self.socket.sendall(command.encode())
        print(f"Sent     : {command.encode()}")

        response = self.socket.recv(1024)
        # print(f"Response : {response.decode(errors='ignore').strip()}")
        print(f"Response : {response}")
        return response

    def close(self):
        if self.socket:
            self.socket.close()
            print("✗ Connection closed.")
