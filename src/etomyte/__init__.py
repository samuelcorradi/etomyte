import os
from etomyte.core.app import Etomyte
from etomyte.adapter.file import FileAdapter

def app(home:str=None
    , port:int=8000
    , adapter:FileAdapter=None
    , default_template:str="index")->Etomyte:
    """
    """
    if not home:
        home = os.getenv("ETOMYTE_HOME", ".")
    app = Etomyte(home, adapter, default_template, port)
    return app