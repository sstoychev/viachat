from .base_command import BaseCommand


class CreateRoom(BaseCommand):

    params = ['name']

    @property
    def action(self):
        return 'createRoom'

    @property
    def describe(self):
        return 'Creates a room'

    def execute():
        pass
