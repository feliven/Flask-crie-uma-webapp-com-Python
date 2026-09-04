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
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import recupera_imagem


@app.route("/")
def index():
    listaJogos = Jogos.query.order_by(Jogos.id)
    return render_template("lista.html", titulo="Lista", jogos=listaJogos)


@app.route("/adicionar-jogo")
def adicionar_jogo():
    if ("usuario_logado" not in session) or (session["usuario_logado"] is None):
        return redirect(url_for("login", proxima=url_for("adicionar_jogo")))

    return render_template("adicionar-jogo.html", titulo="Novo jogo")


@app.route("/criar", methods=["POST"])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]

    novo_jogo = Jogos()
    novo_jogo.nome = nome
    novo_jogo.categoria = categoria
    novo_jogo.console = console

    db.session.add(novo_jogo)
    db.session.commit()

    upload_path = app.config["UPLOAD_PATH"]
    imagem = request.files["imagem"]
    extensao = Path(imagem.filename).suffix if imagem.filename else ""
    imagem.save(f"{upload_path}/capa{novo_jogo.id}{extensao}")

    return redirect(url_for("index"))


@app.route("/editar-jogo/<int:id>")
def editar_jogo(id):
    if ("usuario_logado" not in session) or (session["usuario_logado"] is None):
        return redirect(url_for("login"))

    jogo = Jogos.query.filter_by(id=id).first()

    capa_jogo = recupera_imagem(id)

    return render_template(
        "editar-jogo.html", titulo="Editar jogo", jogo=jogo, capa_jogo=capa_jogo
    )


@app.route("/atualizar", methods=["POST"])
def atualizar():
    id = request.form["id"]
    jogo = Jogos.query.filter_by(id=id).first()

    if jogo:
        jogo.nome = request.form["nome"]
        jogo.categoria = request.form["categoria"]
        jogo.console = request.form["console"]

        db.session.add(jogo)
        db.session.commit()

        upload_path = app.config["UPLOAD_PATH"]
        imagem = request.files["imagem"]
        extensao = Path(imagem.filename).suffix if imagem.filename else ""
        imagem.save(f"{upload_path}/capa{jogo.id}{extensao}")

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


@app.route("/login")
def login():
    proxima = request.args.get("proxima") or "/"
    return render_template("login.html", titulo="Faça seu login", proxima=proxima)


@app.route("/autenticar", methods=["POST"])
def autenticar():
    proxima_pagina = request.form["proxima"]

    listaUsuarios = Usuarios.query.order_by(Usuarios.nickname)

    nickname = request.form["usuario"]
    senha = request.form["senha"]
    listaNicknames = [usuario.nickname for usuario in listaUsuarios]
    listaSenhas = [usuario.senha for usuario in listaUsuarios]

    try:
        if (nickname in listaNicknames) and (
            listaNicknames.index(nickname) == listaSenhas.index(senha)
        ):
            session["usuario_logado"] = nickname
            flash(f"Usuário {nickname} logado com sucesso")
            return (
                redirect(proxima_pagina)
                if proxima_pagina
                else redirect(url_for("index"))
            )
        else:
            flash("Usuário não logado")
            return redirect(url_for("login"))
    except Exception:
        flash("Erro no login")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso.")
    return redirect(url_for("index"))
