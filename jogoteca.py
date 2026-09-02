from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo:
    def __init__(self, nome, categoria, console) -> None:
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo(nome="Tetris", categoria="Puzzle", console="Atari 2600")
jogo2 = Jogo(nome="Hollow Knight", categoria="Metroidvania", console="PS5")
listaJogos = [jogo1, jogo2]


class Usuario:
    def __init__(self, nome, nickname, senha) -> None:
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Felipe", "fvs", "1234")
usuario2 = Usuario("Bruno", "bd", "asdf")
usuario3 = Usuario("Laila", "dog", "hjkl")
listaUsuarios = [usuario1, usuario2, usuario3]

app = Flask(__name__)
app.secret_key = "CHAVE"


@app.route("/")
def index():
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
    jogo = Jogo(nome, categoria, console)
    listaJogos.append(jogo)
    return redirect(url_for("index"))


@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", titulo="Faça seu login", proxima=proxima)


@app.route("/autenticar", methods=["POST"])
def autenticar():
    proxima_pagina = request.form["proxima"]

    nickname = request.form["usuario"]
    senha = request.form["senha"]
    listaNicknames = [usuario.nickname for usuario in listaUsuarios]
    listaSenhas = [usuario.senha for usuario in listaUsuarios]

    if (nickname in listaNicknames) and (
        listaNicknames.index(nickname) == listaSenhas.index(senha)
    ):
        session["usuario_logado"] = nickname
        flash(f"Usuário {nickname} logado com sucesso")
        return (
            redirect(proxima_pagina) if proxima_pagina else redirect(url_for("index"))
        )
    else:
        flash("Usuário não logado")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso.")
    return redirect(url_for("index"))


app.run(debug=True, port=8000)
