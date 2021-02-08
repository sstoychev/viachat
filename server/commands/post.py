from .basecommand import BaseCommand


class Post(BaseCommand):

    @property
    def errors(self):
        return {
            'message_required': 'Message is required',
            'select_room': 'No room selected, select room with /room <room>'
        }

    @property
    def action(self):
        return 'post'

    @property
    def describe(self):
        return 'Posts message to specific room. Last 100 messages are kept and can be retrieved'

    def check(self, msg: str, _username: str) -> str:
        """
        check if we have any message
        """

        if not msg:
            return self.errors['message_required']

        return ''  # no errors

    def execute(self, conn, srv_obj, msg, username: str = ''):
        msg = self.check(msg, username)
        room = srv_obj.addr_users[username]['current_room']
        self.db.insert('rooms_messages', [[room, username, msg]])
        room_msg = f'{username}@{self.room_prefix.replace("room", room)}: {msg}'
        srv_obj.notify(room, room_msg, username)
        # keep only 100 messages per room
        count = list(self.db.select('rooms_messages', {'room': room}, True))  # 1 record, no need of generator
        if count[0][0] >= 100:
            self.db.delete('rooms_messages', {'room': room}, 'id', 1)
