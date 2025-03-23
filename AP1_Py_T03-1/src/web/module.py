from src.domain.service import DomainService
from src.di.container import Container

class WebSession:
    def __init__(self, container: Container):
        self.container = container
        self.domain_service = DomainService()

    def save(self):
        self.container.save(self.domain_service)
