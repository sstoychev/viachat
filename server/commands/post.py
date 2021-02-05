from .base_command import BaseCommand


class Post(BaseCommand):

    @property
    def action(self):
        return 'post'

    @property
    def describe(self):
        return 'Posts message to specific room'

    def check(self, data: str):
        """
        check if we have any message
        """

        if len(data.split(' ')) < 2:
            return 'Message is required'

        return ''  # no errors

    def execute():
        return 'To execute post'
