from flask import Flask, render_template

app = Flask(__name__)


class Jogo:
    def __init__(self, nome, categoria, console) -> None:
        self.nome = nome
        self.categoria = categoria
        self.console = console


@app.route("/inicio")
def ola():
    return "<h1>olá mundo</h1>"


@app.route("/lista")
def lista():
    jogo1 = Jogo(nome="Tetris", categoria="Puzzle", console="Atari 2600")
    jogo2 = Jogo(nome="Hollow Knight", categoria="Metroidvania", console="PS5")
    listaJogos = [jogo1, jogo2]

    return render_template("lista.html", titulo="Lista", jogos=listaJogos)


app.run(debug=True)
