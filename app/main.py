from fastapi import FastAPI
from . import models
from .db import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
models.Base.metadata.create_all(bind=engine) # sqlalchemy models are created, may remove after setting up alembic

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# async def main():
#     return {"message": "Hello World"}

# import psycopg2 as pg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:
#     try:
#         conn = pg2.connect(host='localhost', database='fastapi', user='postgres',
#          password='12345678', cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("db connection succesfull!")
#         break
#     except Exception as error:
#         print("cdb connection failed!")
        # print("Error: ", error)
#         time.sleep(2)


# my_posts=[
#     {"title":"wiafu_1", "content":"bunny_girl_senpai", "id":1},
#     {"title":"waifu_2", "content":"asuma_SAO", "id":2},
#     {"title":"waifu_3", "content":"sakura", "id":3}
#     ]


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)