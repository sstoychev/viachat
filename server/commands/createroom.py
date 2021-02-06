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
        return 'createoom'

    @property
    def describe(self):
        return 'Creates a room'

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
        # if name in rooms:
        #     return 'The room alredy exists'

        return ''  # no errors

    def execute(self, conn, data):
        return 'To execute create room'
