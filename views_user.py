from flask import flash, redirect, render_template, request, session, url_for
from flask_bcrypt import check_password_hash
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

    lista_usuarios = Usuarios.query.order_by(Usuarios.nickname)

    nickname = form.nickname.data
    senha = form.senha.data
    lista_nicknames = [usuario.nickname for usuario in lista_usuarios]
    lista_senhas = [usuario.senha for usuario in lista_usuarios]

    try:
        index_nickname = lista_nicknames.index(nickname)
        senha_para_checar = lista_senhas[index_nickname]

        if check_password_hash(senha_para_checar, senha):
            session["usuario_logado"] = nickname
            flash(f"Usuário {nickname} logado com sucesso")
            return (
                redirect(proxima_pagina)
                if proxima_pagina
                else redirect(url_for("index"))
            )
        else:
            flash("Senha incorreta")
            return redirect(url_for("login"))
    except Exception:
        flash("Erro no login")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso.")
    return redirect(url_for("index"))
