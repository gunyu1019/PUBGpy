class BaseModel:
    def __init__(self, data):
        self.data = data

    def __dict__(self):
        return self.data
