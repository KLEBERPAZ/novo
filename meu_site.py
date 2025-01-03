from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)



app.secret_key = 'sua_chave_secreta_aqui'  # Substitua por uma chave secreta segura

# Usuário fictício para demonstração
USUARIO = {
    "username": "123",
    "password": "123"
}

# Lista para armazenar apostas
apostas = []

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
        if username == USUARIO['username'] and password == USUARIO['password']:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Login inválido. Tente novamente."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/place_bet', methods=['GET', 'POST'])
def place_bet():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        evento = request.form['evento']
        valor = request.form['valor']
        aposta = {'evento': evento, 'valor': valor}
        apostas.append(aposta)
        return redirect(url_for('view_bets'))
    
    return render_template('place_bet.html')

@app.route('/view_bets')
def view_bets():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('view_bets.html', apostas=apostas)

if __name__ == '__main__':
    app.run(debug=True)






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
