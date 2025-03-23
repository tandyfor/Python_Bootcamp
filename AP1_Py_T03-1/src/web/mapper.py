from src.web.model import WebModel
from src.domain.model import DomainModel


class WebMapper:
    @staticmethod
    def web_model_2_domin_model(model: WebModel):
        result = DomainModel()
        result.uuid = model.uuid
        result.board = model.board
        return result

    @staticmethod
    def domain_model_2_web_model(model: DomainModel):
        result = WebModel()
        result.uuid = model.uuid
        result.board = model.board
        result.status = model.game_over()
        return result

    @staticmethod
    def web_model_2_json(model: WebModel):
        result = {
            "uuid" : model.uuid,
            "board" : model.board,
            "status" : model.status
        }
        return result

    @staticmethod
    def json_2_web_model(obj):
        result = WebModel()
        result.uuid = obj.get('uuid')
        result.board = obj.get('board')
        return result
    
    @staticmethod
    def domain_model_2_json(model):
        return WebMapper.web_model_2_json(WebMapper.domain_model_2_web_model(model))
    
