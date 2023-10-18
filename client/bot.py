from client.iclient import IClient

class Bot(IClient):
    def __init__(self):
        super().__init__()
        raise NotImplementedError