import importlib.util
from pathlib import Path
from fastapi import FastAPI

class Server():
    """
    Servidor para a aplicação Etomyte.
    """
    def __init__(self, host:str='127.0.0.1', port:int=8000):
        self.host = host
        self.port = port
        self.app = FastAPI(title="Etomyte", description="Etomyte CMS server")
      