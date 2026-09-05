import os
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class FormularioJogo(FlaskForm):
    nome = StringField(
        "Nome do jogo", [validators.data_required(), validators.length(1, 50)]
    )
    categoria = StringField(
        "Categoria", [validators.data_required(), validators.length(1, 40)]
    )
    console = StringField(
        "Plataforma", [validators.data_required(), validators.length(1, 20)]
    )
    salvar = SubmitField()


class FormularioUsuario(FlaskForm):
    nickname = StringField(
        "Nome de usuário", [validators.data_required(), validators.length(1, 8)]
    )
    senha = PasswordField(
        "Senha", [validators.data_required(), validators.length(1, 100)]
    )
    login = SubmitField()


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config["UPLOAD_PATH"]):
        if f"capa{id}" in nome_arquivo:
            return nome_arquivo

    return "capa_padrao.jpg"


def deleta_imagem(id):
    arquivo = recupera_imagem(id)
    if "capa_padrao" not in arquivo:
        os.remove(os.path.join(app.config["UPLOAD_PATH"], arquivo))
