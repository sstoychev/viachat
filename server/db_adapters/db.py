from abc import ABC, abstractmethod


class Db(ABC):

    @abstractmethod
    def select(self, table: str, conditions: dict) -> list:
        """
        Get data from the table
        """
        pass

    @abstractmethod
    def insert(self, table: str, items: list) -> bool:
        """
        Inserts records in the table
        """
        pass

    @abstractmethod
    def delete(self, table: str, conditions: dict) -> bool:
        """
        Delete table by certain condtitions
        """
        pass

    # # TODO(Stoycho) - should be implemented in
    # @abstractmethod
    # def update(...):
    #     """
    #     Updates rows in the table
    #     """
    #     pass
