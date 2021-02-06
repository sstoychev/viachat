from .basecommand import BaseCommand


class Room(BaseCommand):

    @property
    def errors(self):
        return {
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess'
        }

    @property
    def action(self):
        return 'room'

    @property
    def describe(self):
        return 'Joins a room'

    def check(self, params: str):
        """
        check if we have second parameter and only second
        check if the room name is available
        """

        if not params:
            return self.errors['incorrect_name']

        if len(params.split(' ')) > 1:
            return self.errors['spaces_not_allowed']

        room = list(self.db.select('rooms', {'name': params}))
        if not room:
            return 'The room does not exist'

        return ''  # no errors

    def execute(self, conn, name, username: str = ''):
        self.db.insert('rooms_users', [[name, username]])
        room = list(self.db.select('rooms', {'name': name}))
        return name, f'{self.response_prefix} Welcome to <{name}> created by {room[0][2]}'
