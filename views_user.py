from flask import flash, redirect, render_template, request, session, url_for
from app import app
from models import Usuarios
from helpers import FormularioUsuario


@app.route("/login")
def login():
    proxima = request.args.get("proxima") or "/"

    form = FormularioUsuario()

    return render_template(
        "login.html", titulo="Faça seu login", proxima=proxima, form=form
    )


@app.route("/autenticar", methods=["POST"])
def autenticar():
    form = FormularioUsuario(request.form)

    if not form.validate_on_submit():
        flash("Dados inválidos no formulário")
        return redirect(url_for("login"))

    proxima_pagina = request.form["proxima"]

    listaUsuarios = Usuarios.query.order_by(Usuarios.nickname)

    nickname = form.nickname.data
    senha = form.senha.data
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
