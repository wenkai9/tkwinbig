from abc import ABCMeta, abstractmethod


class DBInterface(metaclass=ABCMeta):
    @abstractmethod
    def connect(self, host, port, user, password, database):
        pass

    @abstractmethod
    def insert(self, table, data):
        pass

    @abstractmethod
    def select(self, table, condition=None):
        pass

    @abstractmethod
    def update(self, table, newdata, condition):
        pass

    @abstractmethod
    def delete(self, table, condition):
        pass