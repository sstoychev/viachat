from .base_command import BaseCommand


class Room(BaseCommand):

    params = ['name']

    @property
    def action(self):
        return 'room'

    @property
    def describe(self):
        return 'Joins a room'

    def execute():
        pass
