from .basecommand import BaseCommand


class CreateRoom(BaseCommand):

    @property
    def errors(self):
        return {
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess'
        }

    @property
    def action(self):
        return 'createroom'

    @property
    def describe(self):
        return 'Creates a room'

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
        if room:
            return 'The room already exists'

        return ''  # no errors

    def execute(self, conn, name, username: str = ''):
        self.db.insert('rooms', [[name, username]])
        return name, f'{self.response_prefix} reated room <{name}>'
