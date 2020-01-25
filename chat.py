import socket
import sys
import time

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    for i in range(5):
        # Connect to server and send data
        sock.sendall(bytes(f"{i}: {data}\n", "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")

        print("Sent:     {}".format(data))
        print("Received: {}".format(received))
        time.sleep(2)
