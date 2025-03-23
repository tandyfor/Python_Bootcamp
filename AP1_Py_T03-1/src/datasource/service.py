from src.datasource.repository import Repository
from src.datasource.mapper import DataMapper


class DataService:
    def __init__(self, repos: Repository):
        self.repos = repos

    def save(self, model):
        self.repos.add(DataMapper.domain_2_data(model))        

    def get(self, uuid):
        return DataMapper.data_2_domain(self.repos.get(uuid))