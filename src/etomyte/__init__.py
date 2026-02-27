import os
from etomyte.core.app import Etomyte

def app(home:str=None)->Etomyte:
    """
    """
    if not home:
        home = os.getenv("ETOMYTE_HOME", ".")
    app = Etomyte(home)
    return app