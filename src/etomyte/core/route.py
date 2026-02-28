"""
Decorador de rotas agnóstico ao framework.
Uso no routes.py do projeto:
```python
from etomyte.core import route
@route("GET", "/hello")
async def hello():
    return {"message": "Hello from Etomyte!"}
@route("POST", "/data")
async def create_data(body: dict):
    return {"created": True}
```
O decorador NÃO depende do FastAPI
— limita-se a anotar a função com
metadados (_etomyte_route).
É o Etomyte.load_routes() que lê essas
anotações e as converte para rotas do
framework subjacente.
"""

# atributo usado internamente para marcar funções decoradas
_ROUTE_ATTR = "_etomyte_route"

def route(method:str, path:str):
    """
    Marca uma função como handler de rota HTTP.
    :param method: Método HTTP (GET, POST, PUT, DELETE, PATCH, etc.)
    :param path: Caminho da rota (ex: "/hello", "/users/{user_id}")
    """
    def decorator(func):
        setattr(func, _ROUTE_ATTR, {
            "method": method.upper(),
            "path": path,
        })
        return func
    return decorator

def get_marked_routes(module) -> list:
    """
    Percorre todos os atributos de um módulo
    e devolve uma lista de tuplos (route_info,
    handler) para cada função marcada com @route.
    """
    routes = []
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and hasattr(obj, _ROUTE_ATTR):
            routes.append((getattr(obj, _ROUTE_ATTR), obj))
    return routes
