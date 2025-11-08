import socket

IP = "192.168.0.2"
PORT = 12289

def tcp_conn(command):
    """Send a TCP command to the specified IP and port, and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)  # setting timeout
        s.connect((IP, PORT))
        print(f"✓ successfully connected to {IP}:{PORT}")
        
        s.sendall(command.encode())#convert string command to bytes
        print(f"Sent : {command.encode()}")
        
        try:
            response = s.recv(1024)
            print(f"Response : {response.decode()}")
            # print(f"Response : {response.hex()}")
        except socket.timeout:
            print("⚠️  No response (timeout)")
            return None
    return response

# class PLCConnection:# Modified the function above to class
#     def __init__(self, ip="192.168.0.2", port=12289, timeout=5.0):
#         self.ip = ip
#         self.port = port
#         self.timeout = timeout
#         self.socket = None

#     def connect(self):
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.settimeout(self.timeout)
#         self.socket.connect((self.ip, self.port))
#         print(f"✓ Connected to {self.ip}:{self.port}")

#     def send(self, command: str):
#         """Send an ASCII command, return response as bytes"""
#         self.socket.sendall(command.encode())
#         print(f"Sent     : {command.encode()}")

#         response = self.socket.recv(1024)
#         # print(f"Response : {response.decode(errors='ignore').strip()}")
#         # print(f"Response : {response.decode()}")
#         return response

#     def close(self):
#         if self.socket:
#             self.socket.close()
#             print("✗ Connection closed.")