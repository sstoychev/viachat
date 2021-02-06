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

    def check(self, data: str):
        """
        No checks are needed. If there is a message it will be send
        """
        return ''  # no errors

    def execute(self, conn, message: str, username: str = ''):
        # TODO(Stoycho) - notify all in the room(s)
        self.db.delete('users', {'addr': str(conn.getpeername())})
        self.db.delete('rooms_users', {'username': str(conn.getpeername())})
        return f'So Long, and Thanks for All the Fish'
