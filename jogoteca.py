from flask import Flask, render_template, request, redirect, session, flash, url_for
from dotenv import load_dotenv
import os

load_dotenv()


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo("Tetris", "Puzzle", "Atari")
jogo2 = Jogo("God of War", "Hack n Slash", "PS2")
jogo3 = Jogo("Mortal Kombat", "Luta", "PS2")
lista = [jogo1, jogo2, jogo3]


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuarios = {}
users_env = os.getenv("USERS", "")
if users_env:
    for user_data in users_env.split(","):
        nome, nickname, senha = user_data.split(":")
        usuarios[nickname] = Usuario(nome, nickname, senha)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")


@app.route("/")
def index():
    return render_template("lista.html", titulo="Jogos", jogos=lista)


@app.route("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login", proxima=url_for("novo")))
    return render_template("novo.html", titulo="Novo Jogo")


@app.route(
    "/criar",
    methods=[
        "POST",
    ],
)
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for("index"))


@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)


@app.route(
    "/autenticar",
    methods=[
        "POST",
    ],
)
def autenticar():
    if request.form["usuario"] in usuarios:
        usuario = usuarios[request.form["usuario"]]
        if request.form["senha"] == usuario.senha:
            session["usuario_logado"] = usuario.nickname
            flash(usuario.nickname + " logado com sucesso!")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
    flash("Usuário não logado.")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
