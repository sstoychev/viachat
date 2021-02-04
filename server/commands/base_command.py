from abc import ABC, abstractmethod

# https://youtu.be/cKPlPJyQrt4?t=1780


class BaseCommand(ABC):

    subclasses = []

    @classmethod
    def __init_subclass__(cls, *a, **kwargs):
        super().__init_subclass__(*a, **kwargs)
        cls.subclasses.append(cls)

    COMMAND_PREFIX = '/'

    params = []

    @property
    @abstractmethod
    def action(self):
        """
        The action term. Example:
        action = 'post', the whole command should be '/post'
        """
        pass

    @property
    @abstractmethod
    def describe(self):
        """
        describe what the command is actually doing
        """
        pass

    def check(self, data):
        """
        checks if the data should be executed with this command
        """
        return data.startswith(f'{self.COMMAND_PREFIX}{self.action} ')

    @abstractmethod
    def execute(self, client):
        pass
