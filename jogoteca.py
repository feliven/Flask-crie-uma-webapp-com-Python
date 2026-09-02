from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = "CHAVE"


class Jogo:
    def __init__(self, nome, categoria, console) -> None:
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo(nome="Tetris", categoria="Puzzle", console="Atari 2600")
jogo2 = Jogo(nome="Hollow Knight", categoria="Metroidvania", console="PS5")
listaJogos = [jogo1, jogo2]


@app.route("/")
def index():
    return render_template("lista.html", titulo="Lista", jogos=listaJogos)


@app.route("/adicionar-jogo")
def adicionar_jogo():
    if ("usuario_logado" not in session) or (session["usuario_logado"] is None):
        return redirect("/login?proxima=adicionar-jogo")

    return render_template("adicionar-jogo.html", titulo="Novo jogo")


@app.route("/criar", methods=["POST"])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome, categoria, console)
    listaJogos.append(jogo)
    return redirect("/")


@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", titulo="Faça seu login", proxima=proxima)


@app.route("/autenticar", methods=["POST"])
def autenticar():
    proxima_pagina = request.form["proxima"]
    print(proxima_pagina)

    if "alohomora" == request.form["senha"]:
        session["usuario_logado"] = request.form["usuario"]
        flash(f'Usuário {session["usuario_logado"]} logado com sucesso')
        return redirect(f"/{proxima_pagina}") if proxima_pagina else redirect("/login")
    else:
        flash("Usuário não logado")
        return redirect("/login")


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso.")
    return redirect("/")


app.run(debug=True, port=8000)
