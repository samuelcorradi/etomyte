import os
from etomyte.core.app import Etomyte

def app(home:str=None)->Etomyte:
    """
    """
    app = Etomyte(home or os.getenv("ETOMYTE_HOME", "."))
    return app