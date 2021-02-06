#!/usr/bin/env python3
# Python program to implement client side of chat room.
import socket
import select
import sys
import os


def handle_event(server: socket.socket, read_sockets):
    for socks in read_sockets:
        if socks == server:
            message = str(socks.recv(2048), "utf-8")
            if not message:
                print('Connection to server lost')
                return False
            print(message)
        else:
            message = sys.stdin.readline().rstrip()
            server.send(bytes(message, "utf-8"))
            if message.split(' ')[0] == '/quit':
                return False
    return True


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print(f'Correct usage:\n{os.path.basename(__file__)} <ip> <port>')
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    """ There are two possible input situations. Either the
    user wants to give manual input to send to other people,
    or the server is sending a message to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])
    if not handle_event(server, read_sockets):
        break

server.close()
