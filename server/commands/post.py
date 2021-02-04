from .base_command import BaseCommand


class Post(BaseCommand):

    params = ['room']

    @property
    def action(self):
        return 'post'

    @property
    def describe(self):
        return 'Posts message to specific room'

    def execute():
        pass
