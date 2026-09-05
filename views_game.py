import time
from pathlib import Path
from flask import (
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
    send_from_directory,
)
from app import app, db
from models import Jogos
from helpers import recupera_imagem, deleta_imagem, FormularioJogo


@app.route("/")
def index():
    listaJogos = Jogos.query.order_by(Jogos.id)
    return render_template("lista.html", titulo="Lista", jogos=listaJogos)


@app.route("/adicionar-jogo")
def adicionar_jogo():
    if ("usuario_logado" not in session) or (session["usuario_logado"] is None):
        return redirect(url_for("login", proxima=url_for("adicionar_jogo")))

    form = FormularioJogo()

    return render_template("adicionar-jogo.html", titulo="Novo jogo", form=form)


@app.route("/criar", methods=["POST"])
def criar():
    form = FormularioJogo()

    if not form.validate_on_submit():
        flash("Dados inválidos no formulário")
        return redirect(url_for("adicionar_jogo"))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    novo_jogo = Jogos()
    novo_jogo.nome = nome
    novo_jogo.categoria = categoria
    novo_jogo.console = console

    db.session.add(novo_jogo)
    db.session.commit()

    upload_path = app.config["UPLOAD_PATH"]
    imagem = request.files.get("imagem")
    if imagem and imagem.filename:
        extensao = Path(imagem.filename).suffix
        timestamp = time.time()
        imagem.save(f"{upload_path}/capa{novo_jogo.id}-{timestamp}{extensao}")

    return redirect(url_for("index"))


@app.route("/editar-jogo/<int:id>")
def editar_jogo(id):
    if ("usuario_logado" not in session) or (session["usuario_logado"] is None):
        return redirect(url_for("login"))

    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()

    if jogo:
        form.nome.data = jogo.nome
        form.categoria.data = jogo.categoria
        form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)

    return render_template(
        "editar-jogo.html",
        titulo="Editar jogo",
        id=id,
        form=form,
        capa_jogo=capa_jogo,
    )


@app.route("/atualizar", methods=["POST"])
def atualizar():
    form = FormularioJogo(request.form)
    id = request.form["id"]

    if not form.validate_on_submit():
        flash("Dados inválidos no formulário")
        return redirect(url_for("editar_jogo", id=id))

    jogo = Jogos.query.filter_by(id=id).first()

    if jogo:
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        upload_path = app.config["UPLOAD_PATH"]
        imagem = request.files.get("imagem")
        if imagem and imagem.filename:
            extensao = Path(imagem.filename).suffix
            timestamp = time.time()
            deleta_imagem(jogo.id)
            imagem.save(f"{upload_path}/capa{jogo.id}-{timestamp}{extensao}")

    return redirect(url_for("index"))


@app.route("/deletar-jogo/<int:id>")
def deletar_jogo(id):
    if ("usuario_logado" not in session) or (session["usuario_logado"] is None):
        return redirect(url_for("login"))

    Jogos.query.filter_by(id=id).delete()

    db.session.commit()

    return redirect(url_for("index"))


@app.route("/uploads/<nome_arquivo>")
def imagem(nome_arquivo):
    return send_from_directory("uploads", nome_arquivo)
