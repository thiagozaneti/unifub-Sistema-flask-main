from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:thiago06102006@localhost/sistemaflask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sistemaflaskchave'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class UserProfessor(db.Model, UserMixin):
    __tablename__ = "userprofessor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cademail = db.Column(db.String(200), unique=True, nullable=False)
    cadcargo = db.Column(db.String(200), nullable=False)
    cadprinome = db.Column(db.String(200), nullable=False)
    cadultname = db.Column(db.String(200), nullable=False)
    cadidentificador = db.Column(db.String(5), unique=True, nullable=False)
    cadsenha = db.Column(db.String(10), nullable=False)
    cadtelefone = db.Column(db.String(11), nullable=False)

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return UserProfessor.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/areadoaluno')
def portalaluno():
    return render_template('portalaluno.html')

@app.route("/areadoprofessor", methods=['POST', 'GET'])
def portalprofessor():
    message = ""
    if request.method == "POST":
        cadprinome = request.form['primeironome']
        cadultname = request.form['segundonome']
        cadidentificador = request.form['identificador']
        cadsenha = request.form['senha']

        userlogin = UserProfessor.query.filter_by(cadprinome=cadprinome, cadultname=cadultname, cadidentificador=cadidentificador, cadsenha=cadsenha).first()

        if userlogin:
            login_user(userlogin)
            resp = make_response(render_template('dsProf.html'))
            resp.set_cookie('usernamecookie', cadprinome)
            return resp
        if not userlogin:
            message = "Usuário inválido, tente novamente"
            return render_template('portalprofessor.html', message=message)

    return render_template("portalprofessor.html")

@app.route("/dsProfessor")
@login_required
def dsProfessor():
    name = request.cookies.get('usernamecookie')
    return render_template("dsProf.html", name=name)

@app.route("/cadastro_professor", methods = ['POST', 'GET'] )
def cadastro_professor():
    if request.method == "POST":
        cademail = request.form['cad_email_prof']
        cadsenha = request.form['cad_senha_prof']
        cadprinome = request.form['cad_priname_prof']
        cadultname = request.form['cad_ultname_prof']
        cadtelefone = request.form['cad_telefone_prof']
        cadcargo = request.form['cad_cargo_prof']
        cadidentificador = request.form['cad_identificador_prof']
    else:
        new_user_professor = UserProfessor(cademail=cademail, cadsenha=cadsenha, cadprinome=cadprinome, cadultname=cadultname, cadtelefone=cadtelefone, cadcargo=cadcargo, cadidentificador=cadidentificador)
        db.session.add(new_user_professor)
        db.session.commit()
        message = "Cadastro realizado com sucesso"
    return render_template('cadprofds.html', message=message)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
