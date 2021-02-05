#!/usr/bin/env python3
import selectors
import socket
# import this explicitly so we can use its .subclasses
from commands.base_command import BaseCommand
# Maybe import * is not the best way
# TODO(Stoycho) review import *
from commands import *

ENC = 'utf-8'  # encoding

COMMAND_PREFIX = '/'
DEFAULT_CMD = f'{COMMAND_PREFIX}post'

motd = 'Welcome to ViaChat!'
available_commands = ['available commands:']

# get all available commands so we can use them when we get message.
cmds = {}
for cls in BaseCommand.subclasses:
    cmd = cls()  # create an instance of the command and add it to the dictionary
    whole_command = f'{COMMAND_PREFIX}{cmd.action}'
    available_commands.append(f'{whole_command} - {cmd.describe}')
    cmds[whole_command] = cmd

available_commands = "\n".join(available_commands)


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    send(conn, f'{motd}\n{available_commands}\n')


def read(conn, mask):
    data = recv(conn)  # Should be ready
    if data:
        cmd = get_command(data)
        if cmd is None:
            send(conn, available_commands)
        else:
            print('found cmd', cmd.action)
            error = cmd.check(data)
            if error != '':
                send(conn, error)
            else:
                send(conn, data)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


def recv(conn):
    return str(conn.recv(1024), ENC).rstrip()


def send(conn, data):
    conn.send(bytes(data, ENC))


def get_command(data: str):
    # check if the first char is COMMAND_PREFIX, otherwise DEFAULT_CMD
    if not data[0] == COMMAND_PREFIX:
        return cmds[DEFAULT_CMD]
    cmd = data.split(' ')[0]
    return cmds.get(cmd, None)


sel = selectors.DefaultSelector()
sock = socket.socket()
sock.bind(('localhost', 1234))
sock.listen()
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

print('Started')
print(motd, available_commands)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
