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
    return render_template("login.html", titulo="Faça seu login")


@app.route("/autenticar", methods=["POST"])
def autenticar():
    if "alohomora" == request.form["senha"]:
        session["usuario_logado"] = request.form["usuario"]
        flash(f'Usuário {session["usuario_logado"]} logado com sucesso')
        return redirect("/")
    else:
        flash("Usuário não logado")
        return redirect("/login")


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso.")
    return redirect("/")


app.run(debug=True, port=8000)
