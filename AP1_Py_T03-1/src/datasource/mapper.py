from src.domain.model import DomainModel
from src.datasource.model import DataModel

from uuid import UUID

class DataMapper:
    @staticmethod
    def domain_2_data(model: DomainModel):
        return DataModel(str(model.uuid), model.board)

    @staticmethod
    def data_2_domain(model: DataModel):
        result = DomainModel()
        result.uuid = UUID(model.uuid)
        result.board = model.board
        return result