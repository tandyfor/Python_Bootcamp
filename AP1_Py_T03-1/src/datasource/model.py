from threading import Lock


class DataModel:
    def __init__(self, uuid, board: list[list]):
        self.uuid = uuid
        self.board = board

class DataStorage:
    def __init__(self):
        self.storage = dict()
        self.lock = Lock()

    def add(self, model: DataModel):
        with self.lock:
            self.storage[model.uuid] = model.board

    def get(self, uuid):
        uuid = str(uuid)
        with self.lock:
            board = self.storage.get(uuid)
            if board is None:
                raise KeyError(f"Model with UUID {uuid} not found in storage.")
            return DataModel(uuid, board)
