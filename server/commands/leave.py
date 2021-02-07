from .basecommand import BaseCommand


class Leave(BaseCommand):

    @property
    def errors(self):
        return {
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess',
            'not_in_room': 'You are not in this room'
        }

    @property
    def action(self):
        return 'leave'

    @property
    def describe(self):
        return 'Leaves a room'

    def check(self, params: str, username: str) -> str:
        """
        check if we have second parameter and only second
        check if the room is existing
        """

        if not params:
            return self.errors['incorrect_name']

        if len(params.split(' ')) > 1:
            return self.errors['spaces_not_allowed']

        rooms_users = list(self.db.select('rooms_users', {'room': params, 'username': username}))
        if not rooms_users:
            return self.errors['not_in_room']

        return ''  # no errors

    def execute(self, conn, addr_users, name: str, username: str = ''):
        msg = self.check(name, username)
        if not msg:
            self.db.delete('rooms_users', {'room': name, 'username': username})
            msg = f'{self.response_prefix} Left room <{name}>'
        return msg
