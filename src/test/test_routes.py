import pytest
from git_repo.src.etomyte.core.server import Server
from etomyte.core.route import route, get_marked_routes, _ROUTE_ATTR

PROJECT_PATH = "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX"

ROUTES_FILE = PROJECT_PATH + "\\config\\routes.py"

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

def test_load_routes_registers_routes():
    """
    load_routes deve registar as rotas do
    routes.py na instância FastAPI.
    """
    server = Server(port=8000)
    server.load_routes(ROUTES_FILE)
    paths = {r.path for r in server.app.routes}
    assert "/hello" in paths
    assert "/data" in paths

def test_load_routes_correct_methods():
    """
    As rotas registadas devem ter os métodos
    HTTP corretos.
    """
    server = Server(port=8000)
    server.load_routes(ROUTES_FILE)
    route_map = {r.path: r.methods for r in server.app.routes if hasattr(r, "methods")}
    assert "GET" in route_map["/hello"]
    assert "POST" in route_map["/data"]

def test_load_routes_file_not_found():
    """
    load_routes deve lançar FileNotFoundError
    se o ficheiro não existir.
    """
    server = Server(port=8000)
    with pytest.raises(FileNotFoundError):
        server.load_routes("/caminho/inexistente/routes.py")

def test_load_routes_no_handlers(tmp_path):
    """
    load_routes deve imprimir aviso se routes.py
    não tiver @route handlers.
    """
    empty_routes = tmp_path / "routes.py"
    empty_routes.write_text("# ficheiro vazio\nx = 1\n", encoding="utf-8")
    server = Server(port=8000)
    # não deve lançar exceção, apenas aviso
    server.load_routes(str(empty_routes))
