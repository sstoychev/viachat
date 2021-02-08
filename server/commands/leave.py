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

    def execute(self, conn, srv_obj, name: str, username: str = ''):
        msg = self.check(name, username)
        if not msg:
            msg = f'{self.server_prefix} Left room <{name}>'
            self.notify_room(srv_obj, name, username)

        srv_obj.send(conn, msg)

    def notify_room(self, srv_obj, name, username, msg: str = ''):
        self.db.delete('rooms_users', {'room': name, 'username': username})
        if name == srv_obj.addr_users[username]['current_room']:
            srv_obj.addr_users[username]['current_room'] = ''
        # notify the rest of the room
        room_msg = f'{self.room_prefix.replace("room", name)} {username} left {msg}'
        srv_obj.notify(name, room_msg, username)
