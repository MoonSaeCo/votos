from flask import Flask, request, render_template, make_response
from random import randint
import datetime as dt
import jwt
import urna
from config import n_arquivos_pessoas as n_pessoas, lista_canditados, necessidade_mesario, logins
app = Flask(__name__)

# Declarando algumas váriaveis que vão ser utilizadas
key = 'Eleicao20242' 	# Chave para o pyjwt, para quando for salvar os cookies do login
codigos = {} 			# Dicionário onde as chaves vão ficar salvas

# Para ser sincero código só não é uma lista e sim um dicionário, para ser legível
# Mais para frente talvez eu tranforme logo em uma lista, mas antes tenho que fazer uma página para checar código já existentes
opcoes = "" #Adiciona as opções para o index.html colocar quais os votos vão ser utilizados
for i in lista_canditados:
	opcoes += f'{i};'

# Página que retorna os códigos que estão salvos, deixar inativo fora de teste
# Deixo para fazer depois a necessidade dos cookies de login para acessar esse site
# Depois de adicionar a verificação de cookies pode deixar ativo em usos reais
# ~ @app.route('/codigos')
# ~ def ver_codigos():
	# ~ return codigos

# Verifica se a matrícula ou o código está presente em codigos
def verificar_codigos(matricula = "", codigo = ""):
	# Essa função checa por uma chave que tenha ou a matrícula ou o código
	if matricula == "":
		for i in codigos.keys():
			# Os primeiros 6 caracteres da chave sempre são o código
			# Então ele checa se os primeiros 6 caracteres coincidem com o código
			if i[0:6] == codigo:
				return True, i
	elif codigo == "":
		for i in codigos.keys():
			# E depois dos primeiros 6 caracteres vai ser a matrícula
			# Então ele checa se o texto depois do sexto caractere é a matrículla
			if i[6::] == matricula:
				return True, i
	'''
	  Essa função devolve se é verdadeiro ou falso (Se existe ou não nos códigos) e a chave da pessoa
	  Se não tiver ele devolve falso e uma string vazia para manter o padrão de ser tuple
	'''
	return False, ""

# Cria um código para uma mtrícula específica e adiciona em codigos
def criar_codigo(matricula):
	x = str(randint(1, 999999)) 	# x vai ser um código
	x = ("0" * (6 - len(x))) + 		x # Adiciona zeros na frente, apenas caso x não tenha 6 caracteres
	# É para deixar padronizado
	
	# Esse while verifica se o código já está registrado
	while verificar_codigos(codigo = x)[0]: 
		# e recria caso já esteja criado
		x = str(randint(1, 999999))
		x = ("0" * (6 - len(x))) + x
	
	# Cria uma data para o código expirar e não poder mais ser utilizado
	t = dt.datetime.now()
	t = t + dt.timedelta(minutes = 5, seconds = 30)
	# Tempo limiti para uso do código são 5 minutos e 30 segundos
	codigos.update({f'{x}{matricula}': {'t': t, 'matricula': matricula, 'codigo': x}}) # Adiciona o código para codigos
	'''
	  Quando um código é criado a chave que dele vai ser o codigo mais a matrícula
	  Exemplo: matrícula = 123 e código = 123456
	  Então a chave vai ser 123456123
	'''
	return x #Retorna o código para ser entregue ao mesário

# Página padrão, vai ser usada para fazer a votação
@app.route('/')
def index():
	return render_template('index.html', opcoes=opcoes)

# Link onde vai ser mandado uma matrícula para registrar um código
@app.route('/codigo', methods=['POST'])
def codigo():
	# Já declara a codigox, vai armazenar o código
	codigox = str()
	# Obtém os valores da matrícula e verifica se já tem código com ela
	mat = request.values['matricula']
	var = verificar_codigos(matricula = mat)
	# Checa nos arquivos de pessoas se a matrícula ja votou
	# Se já votou interrompe a função retornando um feedback
	for i in range(n_pessoas):
		with open(urna.pasta_dados + f"pessoas{i}.txt") as arq:
			if mat in arq.read():
				return render_template("message.html", mss = f"Matrícula {mat}: voto já computado.")
	'''
	  Se a matrícula já tiver um código
	  Então ele checa se a data expirou
	  Se expirou ele deleta e cria um código novo
	  Se não tiver um código ele só cria
	''' 
	if var[0]:
		if codigos[var[1]]['t'] < dt.datetime.now():# Se o tempo para expirar for antes de agora, ou seja, se já expirou
			codigos.pop(var[1])
			codigox = criar_codigo(mat)
		else:
			codigox = "Já possui código"
			render_template('error.html', mensagem = codigox) #Elisa: ntenho certeza ainda se está certo, mas espero que ele renderize a tela de erro 
	else: codigox = criar_codigo(mat)
	
	return render_template('codigo.html', matricula = mat, codigo = codigox)

@app.route('/mesario', methods=['POST', 'GET'])
def mesario():
	if request.method == 'GET':
		'''
		  Tenta pegar um cookie do login que está salvo
		  Se existir um cookie de login, então ele carrega a página do Mesário
		  Se não carrega a página de login
		  E se der erro carrega a de login também
		'''
		try:
			login = jwt.decode(request.cookies.get('login'), key, algorithms="HS256")
			print(request.cookies.get('login'), login)
			if login in logins:
				return render_template('mesario.html')
			else: return render_template('login_mesario.html')
		except:
			return render_template('login_mesario.html')
	if request.method == 'POST':
		'''
		  Se for post significa que alguém tentou logar
		  Então pega os valores do formulário e transforma em um dicionário
		  
		'''
		resp = make_response(render_template('mesario.html'))
		nome = request.values['nome']
		senha = request.values['senha']
		login = {'nome': nome, 'senha': senha}
		
		
		if login in logins: # Se existir esse usuário em logins ele envia em cookie para o cliente
			resp.set_cookie('login', jwt.encode(login, key, algorithm="HS256"), samesite = 'Lax', max_age = 900)
			# Dura no máximo 15 minutos
			# Não tira o samesite = 'Lax', não sei o que faz, mas só funciona com isso
			return resp
		else:
			return render_template("message.html", mss = "Autenticação Falha.")
	
	
# Tela do upload da votação
@app.route('/upload', methods=['POST'])
def upload():
	# Pega as informações de matrícula e código
	mat = request.values["matricula"]
	cod = request.values["codigo"]
	
	# Se for uma votação com mesário
	if necessidade_mesario:
		
		# Se o código e a matrícula existirem em codigos
		if cod+mat in codigos.keys():
			
			# Se não tiver expirado ainda
			if codigos[cod+mat]['t'] > dt.datetime.now():
				
				# Ele tenta escrever, essa função retorna true ou false
				if urna.escrever_voto(mat, request.values["voto"]):
					# Se der para escrever ele apaga a matrícula e devolve um feedback ao usuário
					codigos.pop(cod+mat)
					return render_template("message.html", mss = f"Matrícula {mat}: Voto realizado com sucesso")
					
				# Se der erro ele devolve um feedback de erro ao usuário
				else:					
					return render_template("message.html", mss = f"Matrícula {mat}: Erro ao contabilizar o voto.\nPor favor, tente novamente mais tarde")
			
			# Se não não tiver expirado, ou seja, tiver expirado
			else: 
				# Então o código é deletado de codigos e é retornado um feedback
				codigos.pop(cod+mat)
				return render_template("message.html", mss = 'Codigo Expirado')
		
		# Se não existir essa matrícula com um o código vai retornar um erro	
		else: 
			return render_template("message.html", mss = f"Erro. Matrícula {mat}: não possui um código.\nSolicite um código ao mesário para votar.\nCaso já tenha recebido um código, verifique se a matrícula ou o código foram digitados corretamente.")
	
	# Se não necessitar de um mesário	
	else:
		# Um for para checar se a matrícula já votou, checa nos arquivos
		for i in range(n_pessoas):
			with open(urna.pasta_dados + f"pessoas{i}.txt") as arq:
				
				# Se a matrícula estiver presente no arquivo retorna um feedback
				if mat in arq.read():
					return f"<h1>Matrícula {mat}: voto já computado.</h1>"
					
		# Só vai chegar nessa parte do código se a pessoa não tiver votado
		# Tenta escrever o voto em um arquivo
		# Se der certo retorna um feedback positivo
		# Se der errado retorn um erro
		if urna.escrever_voto(mat, request.values["voto"]):
				return render_template("message.html", mss = f"Matrícula {mat}: Voto realizado com sucesso")
		else:
			return render_template("message.html", mss = f">Matrícula {mat}: Erro ao contabilizar o voto<br>Por favor, tente novamente mais tarde")
		
def main():
	app.run(host = '0.0.0.0', port = 8080, debug=True)
	
if __name__=="__main__":
	main()

