from etomyte.core.route import route

@route("GET", "/hello")
async def hello():
    return {"message": "hello"}

@route("POST", "/data")
async def data():
    return {"ok": True}
