from .base_command import BaseCommand


class UserName(BaseCommand):

    @property
    def action(self):
        return 'username'

    @property
    def describe(self):
        return 'sets username'

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
        # users = db.get('users')
        # if name in rooms:
        #     return 'The room alredy exists'

        return ''  # no errors

    def execute():
        return 'To execute username'
