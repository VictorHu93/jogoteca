from flask import Flask, render_template, request, redirect

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console
jogo1= Jogo('God of War', 'Rack n Slash', 'PS2')
jogo2= Jogo('Skyrim', 'RPG', 'PS4')
jogo3= Jogo('Valorant', 'Multiplayer', 'PC')
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')

app.run(debug=True, host='0.0.0.0', port=8080)