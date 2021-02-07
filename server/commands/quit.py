from .basecommand import BaseCommand


class Quit(BaseCommand):

    @property
    def errors(self):
        return {
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess'
        }

    @property
    def action(self):
        return 'quit'

    @property
    def describe(self):
        return 'Exits the server and notify in all rooms'

    def check(self, data: str, _username: str) -> str:
        """
        No checks are needed. If there is a message it will be send
        """
        return ''  # no errors

    def execute(self, conn, addr_users, message: str, username: str = ''):
        if username:
            # if we don't have username, there is no way for the user
            # to be in registered or in any room
            self.db.delete('users', {'addr': str(conn.getpeername())})
            self.db.delete('rooms_users', {'username': str(conn.getpeername())})
            del addr_users[username]
            # TODO(Stoycho) - notify all in the room(s)
        return ''
