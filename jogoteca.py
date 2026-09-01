from flask import Flask, render_template

app = Flask(__name__)


@app.route("/inicio")
def ola():
    return "<h1>olá mundo</h1>"


@app.route("/lista")
def lista():
    listaJogos = ["God of War", "Skyrim", "Valorant"]
    return render_template("lista.html", titulo="Lista", jogos=listaJogos)


app.run(debug=True)
