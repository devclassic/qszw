from contextlib import asynccontextmanager
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import TORTOISE_ORM
from controllers import routers
from models import User
from fastapi_pagination import add_pagination


@asynccontextmanager
async def lifespan(app):
    async with RegisterTortoise(app, config=TORTOISE_ORM, generate_schemas=True):
        yield


app = FastAPI(
    title="AI应用管理",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def auth(request: Request, call_next):
    if request.method == "OPTIONS":
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    path = request.url.path
    uncheck = [path.startswith("/init") , path.startswith("/auth")]

    if any(uncheck):
        return await call_next(request)

    token = request.headers.get("token")
    user = await User.get_or_none(token=token, is_admin=True)

    if not user:
        return JSONResponse(content={"success": False, "message": "尚未登陆"})
    else:
        return await call_next(request)


for router in routers:
    app.include_router(router)

add_pagination(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
