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

    def execute(self, conn, srv_obj, message: str, username: str = ''):
        srv_obj.disconnect(conn, username, f'({message})')
