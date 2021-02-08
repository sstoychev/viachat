from .basecommand import BaseCommand


class Room(BaseCommand):

    @property
    def errors(self):
        return {
            'incorrect_name': 'You should supply correct name',
            'spaces_not_allowed': 'The name cannot contain spacess',
            'room_not_exists': 'The room does not exist',
            'already_in_room': 'You are already in the room'
        }

    @property
    def action(self):
        return 'room'

    @property
    def describe(self):
        return 'Joins a room'

    def check(self, params: str, username: str) -> str:
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
            return self.errors['room_not_exists']

        return ''  # no errors

    def execute(self, conn, srv_obj, name: str, username: str = ''):
        msg = self.check(name, username)
        if not msg:
            srv_obj.addr_users[username]['current_room'] = name
            rooms_users = list(self.db.select('rooms_users', {'room': name, 'username': username}))
            # if we are already in just change the room to be the current one
            if not rooms_users:
                self.db.insert('rooms_users', [[name, username]])
                # get the room to get it's creator
                room = list(self.db.select('rooms', {'name': name}))
                # we need this for he post command - the user will always send
                # to the last room he joined
                msg = f'{self.server_prefix} Welcome to {self.room_prefix.replace("room", name)} created by {room[0][2]}'

                # notify the rest of the room
                room_msg = f'{self.room_prefix.replace("room", name)} {username} joined'
                srv_obj.notify(name, room_msg, username)

        srv_obj.send(conn, msg)
