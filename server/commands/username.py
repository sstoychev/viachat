from .basecommand import BaseCommand


class UserName(BaseCommand):

    @property
    def errors(self):
        return {
            'specify_username': 'Please, set you username first',
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess'
        }

    @property
    def action(self):
        return 'username'

    @property
    def describe(self):
        return 'sets username'

    def check(self, params: str):
        """
        check if we have second parameter and only second
        check if the room name is available
        """

        if not params:
            return self.errors['incorrect_name']

        if len(params.split(' ')) > 1:
            return self.errors['spaces_not_allowed']

        user = list(self.db.select('users', {'username': params}))
        if user:
            return 'The username is taken'

        return ''  # no errors

    def execute(self, conn, username: str):
        self.db.insert('users', [[str(conn.getpeername()), username]])
        return username

    def get_username(self, conn):
        user = list(self.db.select('users', {'addr': str(conn.getpeername())}))
        if not user:
            return ''
        return user[0][2]
