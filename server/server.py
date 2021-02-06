import sys
import selectors
import socket


class Server(object):

    def __init__(self, config: dict, cmds: dict, available_commands: str) -> None:
        super().__init__()
        self.sel = selectors.DefaultSelector()
        self.available_commands = available_commands
        self.cmds = cmds

        self.ADDRESS = config['address']
        self.PORT = int(config['port'])
        self.ENC = config['encoding']
        self.COMMAND_PREFIX = config['command_prefix']
        self.DEFAULT_CMD = f"{config['command_prefix']}{config['default_cmd']}"
        self.USERNAME_CMD = f"{config['command_prefix']}{config['username_cmd']}"
        self.MOTD = config['motd']

        self.addr_users = {}

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)
        self.addr_users[addr] = ''
        self.send(conn, f'{self.MOTD}\n{self.available_commands}\n')

    def read(self, conn, mask):
        data = self.recv(conn)  # Should be ready

        if data:
            if self.addr_users[conn.getpeername()] == '' and not data.startswith(self.USERNAME_CMD):
                self.send(conn, self.available_commands)
                return
            cmd = self.get_command(data)
            if cmd is None:
                self.send(conn, self.available_commands)
            else:
                print('found cmd', cmd.action)
                error = cmd.check(data)
                if error != '':
                    self.send(conn, error)
                else:
                    self.send(conn, data)
        else:
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()

    def recv(self, conn):
        return str(conn.recv(1024), self.ENC).rstrip()

    def send(self, conn, data):
        conn.send(bytes(data, self.ENC))

    def get_command(self, data: str):
        # check if the first char is COMMAND_PREFIX, otherwise DEFAULT_CMD
        if not data[0] == self.COMMAND_PREFIX:
            return self.cmds[self.DEFAULT_CMD]
        cmd = data.split(' ')[0]
        return self.cmds.get(cmd, None)

    def handle_stdin(self, _conn, _data):
        message = sys.stdin.readline().rstrip()
        # TODO(Stoycho) - implement more commands
        # - number of users
        # - number of rooms
        # - info about user
        # - etc
        if message == 'quit':
            sys.exit()

    def run(self):
        with socket.socket() as sock:
            sock.bind((self.ADDRESS, self.PORT))
            sock.listen()
            sock.setblocking(False)
            self.sel.register(sock, selectors.EVENT_READ, self.accept)
            self.sel.register(sys.stdin, selectors.EVENT_READ, self.handle_stdin)

            print('Started')
            print(self.MOTD, self.available_commands)

            while True:
                events = self.sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
