from flask import Flask, request, render_template, make_response
from random import randint
import datetime as dt
import jwt
import urna
app = Flask(__name__)

key = 'Eleicao20242'
codigos = {}



logins = [{
	'nome': 'User546',
	'senha': '123'
}]

@app.route('/codigos')
def ver_codigos():
	return codigos

def verificar_codigos(matricula = "", codigo = ""):
	if matricula == "":
		for i in codigos.keys():
			if i[0:6] == codigo:
				return True, i
	elif codigo == "":
		for i in codigos.keys():
			if i[6::] == matricula:
				return True, i
	return False, ""

def criar_codigo(matricula):
	x = str(randint(1, 999999))
	x = ("0" * (6 - len(x))) + x
	while verificar_codigos(codigo = x)[0]:
		x = str(randint(1, 999999))
		x = ("0" * (6 - len(x))) + x
	t = dt.datetime.now()
	t = t + dt.timedelta(minutes = 5, seconds = 30)
	codigos.update({f'{x}{matricula}': {'t': t, 'matricula': matricula, 'codigo': x}})
	return x

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/codigo', methods=['POST'])
def codigo():
	codigox = "Essa Matricula ja tem codigo"
	mat = request.values['matricula']
	var = verificar_codigos(matricula = mat)
	for i in range(urna.n_pessoas):
		with open(urna.pasta_dados + f"pessoas{i}.txt") as arq:
			if mat in arq.read():
				return f"<h1>Matrícula {mat}: voto já computado.</h1>"
				
	if var[0]:
		if codigos[var[1]]['t'] < dt.datetime.now():
			codigos.pop(var[1])
	else: codigox = criar_codigo(mat)
	
	return render_template('codigo.html', matricula = mat, codigo = codigox)

@app.route('/mesario', methods=['POST', 'GET'])
def mesario():
	if request.method == 'GET':
		try:
			login = jwt.decode(request.cookies.get('login'), key, algorithms="HS256")
			print(request.cookies.get('login'), login)
			if login in logins:
				return render_template('mesario.html')
			else: return render_template('login_mesario.html')
		except:
			return render_template('login_mesario.html')
	if request.method == 'POST':
		# ~ try:
		resp = make_response(render_template('mesario.html'))
		nome = request.values['nome']
		senha = request.values['senha']
		login = {'nome': nome, 'senha': senha}
		# ~ print(nome, senha, login, logins)
		
		expire_date = dt.datetime.now() + dt.timedelta(minutes=30)
		
		if login in logins:
			resp.set_cookie('login', jwt.encode(login, key, algorithm="HS256"), samesite = 'Lax', max_age = 900)
			return resp
		else:
			return "<h1>Autenticação Falha.</h1>"
	
	

@app.route('/upload', methods=['POST'])
def upload():
	mat = request.values["matricula"]
	cod = request.values["codigo"]
	if cod+mat in codigos.keys():
		if codigos[cod+mat]['t'] > dt.datetime.now():
			if urna.escrever_voto(mat, request.values["voto"]):
				codigos.pop(cod+mat)
				return f"<h1>Matrícula {mat}: Voto realizado com sucesso</h1>"
			else:
				return f"<h1>Matrícula {mat}: Erro ao contabilizar o voto<br>Por favor, tente novamente mais tarde</h1>"
				
		else:
			codigos.pop(cod+mat)
			return '<h1>Codigo Expirado</h1>'
	return f"<h1>Erro. Matrícula {mat}: não possui um código.<br>Solicite um código ao mesário para votar.<br>Caso já tenha recebido um código, verifique se a matrícula ou o código foram digitados corretamente.</h1>"

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 8080, debug=True)

