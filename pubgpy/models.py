class BaseModel:
    def __init__(self, data):
        self.data = data

    def __dict__(self):
        return self.data


class PUBGModel(BaseModel):
    def __init__(self, _class):
        super().__init__(_class.data)
        self.model_id = _class.model_id
        self.model_type = _class.model_type
    
    def __eq__(self, other):
        return self.model_id == other.id and self.model_type == other.type

    def __ne__(self, other):
        return not self.__eq__(other)