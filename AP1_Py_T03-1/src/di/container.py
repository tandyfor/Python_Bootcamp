from src.datasource.model import DataStorage
from src.datasource.repository import Repository
from src.datasource.service import DataService
from src.domain.service import DomainService

class Container:
    def __init__(self):
        self.storage = DataStorage()
        self.repository = Repository(self.storage)
        self.service = DataService(self.repository)

    def save(self, service: DomainService):
        self.service.save(service.model)

    def get(self, uuid):
        return self.service.get(uuid)