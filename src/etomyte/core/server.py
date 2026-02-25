from fastapi import FastAPI

class Server():
    """
    Servidor para a aplicação Etomyte.
    """
    def __init__(self, port=8000):
        self.port = port
        self.app = FastAPI(title="Etomyte", description="Etomyte CMS server")
        self.__config = {}

    def set_config(self, name:str, value):
        self.__config[name] = value
    
    @property
    def config(self) -> dict:
        return self.__config

    @config.setter
    def config(self, value: dict):
        self.__config = value
