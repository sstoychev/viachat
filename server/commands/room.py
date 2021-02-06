from .basecommand import BaseCommand


class Room(BaseCommand):

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
            return 'You should supply correct name'

        if len(params) > 2:
            return 'The name cannot contain spacess'

        name = params[1]

        # TODO(Stoycho)
        # rooms = db.get('rooms')
        # if name not in rooms:
        #     return 'The room does not exist'

        return ''  # no errors

    def execute():
        return 'To execute room'
