from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOSTNAME=getenv("DATABASE_HOSTNAME")
DATABASE_PORT=getenv("DATABASE_PORT")
DATABASE_PASSWORD=getenv("DATABASE_PASSWORD")
DATABASE_NAME=getenv("DATABASE_NAME")
SECRET_KEY=getenv("SECRET_KEY")
ALGORITHM=getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=getenv("ACCESS_TOKEN_EXPIRE_MINUTES")