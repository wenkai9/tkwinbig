from abc import ABCMeta, abstractmethod


class AssistantInterface(metaclass=ABCMeta):
    @abstractmethod
    def chat(self, table, data):
        pass