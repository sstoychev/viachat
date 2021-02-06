import sys
import selectors
import socket


class Server(object):

    def __init__(self, config: dict, cmds: dict, available_commands: str) -> None:
        super().__init__()

        self.RUN_FOREVER = True

        self.sel = selectors.DefaultSelector()
        self.available_commands = available_commands
        self.cmds = cmds

        self.ADDRESS = config['address']
        self.PORT = int(config['port'])
        self.ENC = config['encoding']
        self.COMMAND_PREFIX = config['command_prefix']
        self.MOTD = config['motd']

        self.POST_CMD = 'post'
        self.QUIT_CMD = 'quit'
        self.USER_CMD = 'username'

        self.addr_users = {}

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)
        self.send(conn, f'{self.MOTD}\n{self.available_commands}\n')

    def read(self, conn, mask):
        data = self.recv(conn)  # Should be ready

        if data:
            # check if we have username for this connection
            username = self.cmds[self.USER_CMD].get_username(conn)

            if not username:
                # /username and /quit are allowed without username set
                if data.startswith(self.COMMAND_PREFIX) and data[1:].startswith((self.USER_CMD, self.QUIT_CMD)):
                    pass
                else:
                    self.send(conn, self.cmds[self.USER_CMD].errors['specify_username'])
                    return

            # check if the data starts with /
            # and if so if it is in the available commands
            cmd, params = self.get_command(data)

            if cmd is None:
                self.send(conn, self.available_commands)
            else:
                # validate command's parameters
                print('found cmd', cmd.action)
                error = cmd.check(params)
                if error != '':
                    self.send(conn, error)
                else:
                    response = cmd.execute(conn, params)
                    # if the user is setting name we have to record it with the connection
                    if cmd.action == self.USER_CMD:
                        self.addr_users[response] = conn
                    if cmd.action == self.QUIT_CMD and username:
                        del self.addr_users[username]
                    if response:
                        self.send(conn, response)
        else:
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()

    def recv(self, conn):
        return str(conn.recv(1024), self.ENC).rstrip()

    def send(self, conn, data):
        conn.send(bytes(data, self.ENC))

    def get_command(self, data: str):
        # check if the first char is COMMAND_PREFIX, otherwise 'post'
        if not data[0] == self.COMMAND_PREFIX:
            return self.cmds[self.POST_CMD]

        cmd = data.split(' ')[0][1:]
        # +2 is for / at the beginning and ' ' after the comman
        params = data[len(cmd)+2:]
        cmd_object = self.cmds.get(cmd, None)
        return cmd_object, params

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
            self.sel.register(
                sys.stdin, selectors.EVENT_READ, self.handle_stdin)

            print('Started')
            print(self.MOTD, self.available_commands)

            while True:
                events = self.sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
