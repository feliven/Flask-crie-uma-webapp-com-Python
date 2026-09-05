import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


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


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config["UPLOAD_PATH"]):
        if f"capa{id}" in nome_arquivo:
            return nome_arquivo

    return "capa_padrao.jpg"


def deleta_imagem(id):
    arquivo = recupera_imagem(id)
    if "capa_padrao" not in arquivo:
        os.remove(os.path.join(app.config["UPLOAD_PATH"], arquivo))
