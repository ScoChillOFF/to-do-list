from fastapi import FastAPI

from .routers.auth import router as auth_router


app = FastAPI()

routers = [
    auth_router,
]

for router in routers:
    app.include_router(router)
