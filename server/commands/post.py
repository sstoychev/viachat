from .basecommand import BaseCommand


class Post(BaseCommand):

    @property
    def errors(self):
        return {
            'message_required': 'Message is required'
        }

    @property
    def action(self):
        return 'post'

    @property
    def describe(self):
        return 'Posts message to specific room'

    def check(self, data: str, _username: str) -> str:
        """
        check if we have any message
        """

        if len(data.split(' ')) < 2:
            return self.errors['message_required']

        return ''  # no errors

    def execute(self, conn, addr_users, data, username: str = ''):
        return 'To execute post'
