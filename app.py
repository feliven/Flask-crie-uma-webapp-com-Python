# cria e configura a aplicação Flask, sem iniciar o servidor

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
