from flask import Flask, render_template

app = Flask(__name__)


@app.route("/inicio")
def ola():
    return "<h1>olá mundo</h1>"


@app.route("/lista")
def lista():
    return render_template("lista.html", title="Lista")


app.run()
