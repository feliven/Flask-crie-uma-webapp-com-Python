from flask import Flask, render_template, request, redirect

app = Flask(__name__)


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
        return redirect("/")
    else:
        return redirect("/login")


app.run(debug=True, port=8000)
