import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(
    SGBD="mysql+mysqlconnector",
    usuario="root",
    senha=os.getenv("SQL_SENHA"),
    servidor="localhost",
    database="jogoteca",
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/uploads"
