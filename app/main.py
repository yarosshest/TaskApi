import asyncio

import uvicorn as uvicorn
from fastapi import FastAPI
from db.database import init_db
from fastapi.security import OAuth2PasswordBearer
from routers.token import router as token
from routers.auth import router as auth
from routers.task import router as task

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api = FastAPI()

api.include_router(token)
api.include_router(auth)
api.include_router(task)


def app_main():
    asyncio.run(init_db())
    # uvicorn.run(api, host="0.0.0.0", port=8031)
    uvicorn.run('main:api', host="0.0.0.0", port=8031, workers=4)


if __name__ == "__main__":
    app_main()
