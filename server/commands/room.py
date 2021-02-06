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

    def check(self, data: str):
        """
        check if we have second parameter and only second
        check if the room name is available
        """

        params = data.split(' ')
        if len(params) == 1:
            return self.errors['incorrect_name']

        if len(params) > 2:
            return self.errors['spaces_not_allowed']

        name = params[1]

        # TODO(Stoycho)
        # rooms = db.get('rooms')
        # if name not in rooms:
        #     return 'The room does not exist'

        return ''  # no errors

    def execute(self, conn, data):
        return 'To execute room'
