from .basecommand import BaseCommand


class UserName(BaseCommand):

    @property
    def errors(self):
        return {
            'specify_username': 'Please, set you username first',
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess',
            'change_not_allowed': 'Change of the username is not allowed'
        }

    @property
    def action(self):
        return 'username'

    @property
    def describe(self):
        return 'sets username'

    def check(self, params: str, username: str) -> str:
        """
        params is actually the new user name
        username should be empty

        check if we have second parameter and only second
        check if the room name is available
        """

        if username:
            return self.errors['change_not_allowed']

        if not params:
            return self.errors['incorrect_name']

        if len(params.split(' ')) > 1:
            return self.errors['spaces_not_allowed']

        user = list(self.db.select('users', {'username': params}))
        if user:
            return 'The username is taken'

        return ''  # no errors

    def execute(self, conn, addr_users, data: str, username: str = ''):
        msg = self.check(data, username)
        if not msg:
            self.db.insert('users', [[str(conn.getpeername()), data]])
            # if the user is setting name we have to record it with the connection
            addr_users[data] = conn
            msg = f'{self.response_prefix} username set to {data}'
        return msg

    def get_username(self, conn):
        user = list(self.db.select('users', {'addr': str(conn.getpeername())}))
        if not user:
            return ''
        return user[0][2]
