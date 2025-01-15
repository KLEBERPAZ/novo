from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Substitua por uma chave secreta segura

# Caminho para o arquivo de visitas
VISITS_FILE = 'visits.txt'

def get_visits():
    if not os.path.exists(VISITS_FILE):
        with open(VISITS_FILE, 'w') as file:
            file.write('0')
    with open(VISITS_FILE, 'r') as file:
        visits = int(file.read())
    return visits

def increment_visits():
    visits = get_visits() + 1
    with open(VISITS_FILE, 'w') as file:
        file.write(str(visits))
    return visits

# Usuário fictício para demonstração
USUARIO = {
    "username": "1",
    "password": "1"
}

# Lista para armazenar apostas
apostas = []

# Lista para armazenar participantes
participantes = []

# Lista para armazenar turmas
turmas = []



@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        tipo_aposta = request.form['tipo_aposta']
        if username == USUARIO['username'] and password == USUARIO['password']:
            session['username'] = username
            session['tipo_aposta'] = tipo_aposta
            visits = increment_visits()
            return render_template('home.html', username=username, visits=visits)
        else:
            return "Login inválido. Tente novamente."
    visits = get_visits()
    return render_template('login.html', visits=visits)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('tipo_aposta', None)
    return redirect(url_for('login'))

@app.route('/place_bet', methods=['GET', 'POST'])
def place_bet():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    tipo_aposta = session.get('tipo_aposta')
    
    if request.method == 'POST':
        if tipo_aposta == "mega_sena":
            numeros = sorted([
                request.form['numero1'],
                request.form['numero2'],
                request.form['numero3'],
                request.form['numero4'],
                request.form['numero5'],
                request.form['numero6']
            ])
        elif tipo_aposta == "loto_facil":
            numeros = sorted([request.form['numero{}'.format(i)] for i in range(1, 16)])
        
        valor = request.form['valor']
        participante = request.form['participante']
        aposta = {'numeros': numeros, 'valor': valor, 'participante': participante, 'tipo_aposta': tipo_aposta}
        apostas.append(aposta)
        return redirect(url_for('view_bets'))
    
    return render_template('place_bet.html', participantes=participantes, tipo_aposta=tipo_aposta)

@app.route('/view_bets')
def view_bets():
    if 'username' not in session:
        return redirect(url_for('login'))

    sorted_apostas = sorted(apostas, key=lambda aposta: aposta['participante'].lower())
    return render_template('view_bets.html', apostas=sorted_apostas)

@app.route('/manage_participants', methods=['GET', 'POST'])
def manage_participants():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        data_aposta = request.form['data_aposta']
        participante = {'nome': nome, 'data_aposta': data_aposta}
        participantes.append(participante)
        return redirect(url_for('manage_participants'))

    return render_template('manage_participants.html', participantes=sorted(participantes, key=lambda p: p['nome'].lower()))

@app.route('/edit_bet/<int:bet_id>', methods=['GET', 'POST'])
def edit_bet(bet_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        tipo_aposta = session.get('tipo_aposta')
        if tipo_aposta == "mega_sena":
            numeros = sorted([
                request.form['numero1'],
                request.form['numero2'],
                request.form['numero3'],
                request.form['numero4'],
                request.form['numero5'],
                request.form['numero6']
            ])
        elif tipo_aposta == "loto_facil":
            numeros = sorted([request.form['numero{}'.format(i)] for i in range(1, 16)])
        
        valor = request.form['valor']
        participante = request.form['participante']
        apostas[bet_id] = {'numeros': numeros, 'valor': valor, 'participante': participante, 'tipo_aposta': tipo_aposta}
        return redirect(url_for('view_bets'))
    
    aposta = apostas[bet_id]
    return render_template('edit_bet.html', aposta=aposta, participantes=participantes, bet_id=bet_id)



@app.route('/edit_participant/<int:participant_id>', methods=['GET', 'POST'])
def edit_participant(participant_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        data_aposta = request.form['data_aposta']
        participantes[participant_id] = {'nome': nome, 'data_aposta': data_aposta}
        return redirect(url_for('manage_participants'))
    
    participante = participantes[participant_id]
    return render_template('edit_participant.html', participante=participante, participant_id=participant_id)



@app.route('/delete_bet/<int:bet_id>', methods=['POST'])
def delete_bet(bet_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 0 <= bet_id < len(apostas):
        del apostas[bet_id]
    return redirect(url_for('view_bets'))

@app.route('/delete_participant/<int:participant_id>', methods=['POST'])
def delete_participant(participant_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 0 <= participant_id < len(participantes):
        del participantes[participant_id]
    return redirect(url_for('manage_participants'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/escola')
def escola():
    return render_template('escola.html')

@app.route('/cadastro_alunos')
def cadastro_alunos():
    return render_template('cadastro_alunos.html')

@app.route('/cadastro_turmas', methods=['GET', 'POST'])
def cadastro_turmas():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        serie = request.form['serie']
        turma = request.form['turma']
        turno = request.form['turno']
        nova_turma = {'serie': serie, 'turma': turma, 'turno': turno}
        turmas.append(nova_turma)
        return redirect(url_for('cadastro_turmas'))

    return render_template('cadastro_turmas.html', turmas=turmas)







if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for, session


# app = Flask(__name__)



# app.secret_key = 'sua_chave_secreta_aqui'  # Substitua por uma chave secreta segura

# # Usuário fictício para demonstração
# USUARIO = {
#     "username": "123",
#     "password": "123"
# }

# # Lista para armazenar apostas
# apostas = []

# @app.route('/')
# def home():
#     if 'username' in session:
#         return render_template('home.html', username=session['username'])
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == USUARIO['username'] and password == USUARIO['password']:
#             session['username'] = username
#             return redirect(url_for('home'))
#         else:
#             return "Login inválido. Tente novamente."
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route('/place_bet', methods=['GET', 'POST'])
# def place_bet():
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         evento = request.form['evento']
#         valor = request.form['valor']
#         aposta = {'evento': evento, 'valor': valor}
#         apostas.append(aposta)
#         return redirect(url_for('view_bets'))
    
#     return render_template('place_bet.html')

# @app.route('/view_bets')
# def view_bets():
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     return render_template('view_bets.html', apostas=apostas)

# if __name__ == '__main__':
#     app.run(debug=True)






# # Lista para armazenar os cadastros
# usuarios = []

# @app.route("/")
# def index():
#     return render_template("index.html", usuarios=usuarios)

# @app.route("/cadastrar", methods=["GET", "POST"])
# def cadastrar():
#     if request.method == "POST":
#         nome = request.form.get("nome")
#         email = request.form.get("email")
#         senha = request.form.get("senha")
        
#         if nome and email and senha:
#             usuarios.append({"nome": nome, "email": email, "senha": senha})
#             return redirect(url_for("index"))
    
#     return render_template("cadastrar.html")

# @app.route("/detalhes/<int:usuario_id>")
# def detalhes(usuario_id):
#     if 0 <= usuario_id < len(usuarios):
#         usuario = usuarios[usuario_id]
#         return render_template("detalhes.html", usuario=usuario, usuario_id=usuario_id)
#     return redirect(url_for("index"))

# @app.route("/especificas")
# def especificas():
#     return render_template("especificas.html")

# @app.route("/nocoesdedireitoconstitucional")
# def nocoesdedireitoconstitucional():
#     return render_template("nocoesdedireitoconstitucional.html")



# @app.route("/nocoesdedireitoadministrativo")
# def nocoesdedireitoadministrativo():
#     return render_template("nocoesdedireitoadministrativo.html")


# @app.route("/linguaportuguesa")
# def linguaportuguesa():
#     return render_template("linguaportuguesa.html")

# @app.route("/estatutodoservidorpublicoestadualeleiorganicadaPGE")
# def estatutodoservidorpublicoestadualeleiorganicadaPGE():
#     return render_template("estatutodoservidorpublicoestadualeleiorganicadaPGE.html")


# @app.route("/excluir/<int:usuario_id>", methods=["POST"])
# def excluir(usuario_id):
#     if 0 <= usuario_id < len(usuarios):
#         del usuarios[usuario_id]
#     return redirect(url_for("index"))



# app.secret_key = 'sua_chave_secreta_aqui'  # Substitua por uma chave secreta segura

# # Usuário fictício para demonstração
# USUARIO = {
#     "username": "usuario123",
#     "password": "senha123"
# }

# @app.route('/')
# def home():
#     if 'username' in session:
#         return render_template('index.html', username=session['username'])
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == USUARIO['username'] and password == USUARIO['password']:
#             session['username'] = username
#             return redirect(url_for('index'))
#         else:
#             return "Login inválido. Tente novamente."
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))


# if __name__ == "__main__":
#     app.run(debug=True)
