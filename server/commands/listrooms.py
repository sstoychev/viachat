from .basecommand import BaseCommand


class ListUsers(BaseCommand):

    @property
    def errors(self):
        return {
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess',
            'not_in_room': 'You are not in this room'
        }

    @property
    def action(self):
        return 'listrooms'

    @property
    def describe(self):
        return 'List available rooms'

    def check(self, params: str, username: str) -> str:
        """
        there is nothing to check
        """
        return ''  # no errors

    def execute(self, conn, addr_users, name: str, username: str = ''):
        msg = self.check(name, username)
        if not msg:
            rooms = self.db.select('rooms')
            msg = '\n'.join([room[1] for room in rooms])
        return msg
