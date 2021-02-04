#!/usr/bin/env python3
import selectors
import socket
from commands.base_command import BaseCommand
from commands import *

motd = ['Welcome to ViaChat!', 'available commands:']

cmds = []
for cls in BaseCommand.subclasses:
    cmd = cls()
    motd.append(f'{cmd.COMMAND_PREFIX}{cmd.action} - {cmd.describe}')
    cmds.append(cmd)


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    conn.send(bytes("\n".join(motd), "utf-8"))


def read(conn, mask):
    data = conn.recv(1024)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


sel = selectors.DefaultSelector()
sock = socket.socket()
sock.bind(('localhost', 12345))
sock.listen()
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
