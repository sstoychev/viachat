from .basecommand import BaseCommand
from .room import Room


class CreateRoom(BaseCommand):

    @property
    def errors(self):
        return {
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess',
            'already_exists': 'The room already exists'
        }

    @property
    def action(self):
        return 'createroom'

    @property
    def describe(self):
        return 'Creates a room and joins it after this'

    def check(self, params: str, _username: str) -> str:
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
            return self.errors['already_exists']

        return ''  # no errors

    def execute(self, conn, srv_obj, name: str, username: str = ''):
        msg = self.check(name, username)
        if not msg:
            self.db.insert('rooms', [[name, username]])
            # TODO(Stoycho) join room after creation
            msg = f'{self.server_prefix} created room <{name}>, </room {name}> to join it'

        srv_obj.send(conn, msg)
