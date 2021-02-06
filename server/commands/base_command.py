from abc import ABC, abstractmethod

# https://youtu.be/cKPlPJyQrt4?t=1780


class BaseCommand(ABC):

    subclasses = []

    @classmethod
    def __init_subclass__(cls, *a, **kwargs):
        super().__init_subclass__(*a, **kwargs)
        cls.subclasses.append(cls)

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

    @abstractmethod
    def check(self, data: str) -> str:
        """
        checks if the data should be executed with this command
        """
        pass

    @abstractmethod
    def execute(self, client):
        pass
