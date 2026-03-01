import pytest
from pathlib import Path
from etomyte.core.route import route, get_marked_routes, _ROUTE_ATTR

def test_route_decorator_marks_function():
    """O decorador deve adicionar o atributo _etomyte_route à função."""
    @route("GET", "/test")
    async def my_handler():
        return {"ok": True}
    assert hasattr(my_handler, _ROUTE_ATTR)
    info = getattr(my_handler, _ROUTE_ATTR)
    assert info["method"] == "GET"
    assert info["path"] == "/test"

def test_route_decorator_uppercases_method():
    """
    O método HTTP deve ser normalizado para maiúsculas.
    """
    @route("post", "/submit")
    async def submit():
        return {}
    info = getattr(submit, _ROUTE_ATTR)
    assert info["method"] == "POST"

def test_route_decorator_preserves_function():
    """
    O decorador não deve alterar a função original.
    """
    @route("GET", "/hello")
    async def hello():
        return {"message": "hi"}
    # a função continua a ser chamável e retorna o esperado
    import asyncio
    result = asyncio.run(hello())
    assert result == {"message": "hi"}

def test_get_marked_routes_from_module():
    """
    get_marked_routes deve encontrar todas as funções
    marcadas num módulo.
    """
    import types
    mod = types.ModuleType("fake_routes")
    # rota de teste 1
    @route("GET", "/a")
    async def handler_a():
        return "a"
    # rota de teste 2
    @route("DELETE", "/b")
    async def handler_b():
        return "b"
    mod.handler_a = handler_a
    mod.handler_b = handler_b
    mod.not_a_route = lambda: None  # não marcada
    marked = get_marked_routes(mod)
    assert len(marked) == 2
    methods = {info["method"] for info, _ in marked}
    assert methods == {"GET", "DELETE"}

def test_load_routes_registers_routes(app, home):
    """
    load_routes deve registar as rotas do
    routes.py na instância FastAPI.
    """
    routes_file = Path(home)/"config"/"routes.py"
    app.load_routes(str(routes_file))
    paths = {r.path for r in app.server.app.routes}
    assert "/hello" in paths
    assert "/data" in paths

def test_load_routes_correct_methods(home, app):
    """
    As rotas registadas devem ter os métodos
    HTTP corretos.
    """
    routes_file = Path(home)/"config"/"routes.py"
    app.load_routes(str(routes_file))
    route_map = {r.path: r.methods for r in app.server.app.routes if hasattr(r, "methods")}
    assert "GET" in route_map["/hello"]
    assert "POST" in route_map["/data"]

def test_load_routes_file_not_found(app):
    """
    load_routes deve lançar FileNotFoundError
    se o ficheiro não existir.
    """
    with pytest.raises(FileNotFoundError):
        app.load_routes("/caminho/inexistente/routes.py")

def test_load_routes_no_handlers(app,tmp_path):
    """
    load_routes deve imprimir aviso se routes.py
    não tiver @route handlers.
    """
    empty_routes = tmp_path / "routes.py"
    empty_routes.write_text("# ficheiro vazio\nx = 1\n", encoding="utf-8")
    # não deve lançar exceção, apenas aviso
    app.load_routes(str(empty_routes))
