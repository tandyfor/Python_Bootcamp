from src.datasource.model import DataStorage


class Repository:
    def __init__(self, storage: DataStorage):
        self.storage = storage

    def add(self, model):
        self.storage.add(model)

    def get(self, uuid):
        return self.storage.get(uuid)