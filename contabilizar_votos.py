from urna import pasta_dados, n_pessoas
from json import load
from hashlib import sha256
from config import lista_canditados
import matplotlib.pyplot as plt
import os
pasta = os.getcwd()

print(pasta_dados)
with open(pasta_dados + "info.json", 'r') as arq:
		print(load(arq))

def main():
	# Declarando votos e colocando as chaves como o nome dos candidatos
	votos = {}
	for i in lista_canditados:
		votos.update({i: 0})
		
	# Declarando info e pegando o seu valor do json: "info.json"
	info = {}
	with open(pasta_dados + "info.json", 'r') as arq:
		info = load(arq)
	
	# Declarando lista_pessoas e obtendo a lista de matrículas de cada pessoa que votou
	# Ele pega o nome dos arquivos pelo info
	# Usar o setup.py (primeira opção do main.py) e ver a estrutura do info.json na pasta dados para entender melhor a estrutura
	# O programa salva na lista matrículas como um hash do sha256, para poder comparar com os votos
	lista_pessoas = []
	for i in info["arquivos_pessoas"]:
		with open(pasta_dados + i['archive_name']) as arq:
			for j in arq.readlines():
				lista_pessoas.append(sha256(j.strip().encode()).hexdigest())
	
	
	# Acessa pelas informações dos nomes dos arquivos em info.json e abre um por um
	for i in info['grupos']:
		with open(pasta_dados + i['archive_name']) as arq:
			# Depois de abrir os arquivos, ele abre linha por linha e analisa, vê o voto e adiciona ao candidato do votos
			# Mas antes checa se a matrícula em hash está em lista_pessoas, para evitar erro de uma matrícula ter sido salva errada
			for j in arq.readlines():
				l = j.strip().split(":")
				if l[1] in lista_pessoas:
					votos[l[0]] += 1
	# ~ print(f"Chapa 1: {votos['1']}\nChapa 2: {votos['2']}\nChapa 3: {votos['3']}\nChapa 4:{votos['4']}")
	
	# labels é uma lista que vai ser passada para o matlib criar um gráficos
	# labels vai conter o nome dos candidatos, ele pega essa informação direto das chaves de votos
	labels = list()
	# ~ dic = dict()
	for i in votos.keys():
		labels.append(str(i))
		# ~ dic.update({str(i): votos[i]})
	
	# Declara a lista x e adiciona os votos nela
	# x vai ser usado para criar o gráfico
	x = list()
	for i in votos.keys():
		x.append(votos[i])
	
	# Cria o gráfico de pizza e salva ele como: "votos.png"
	# "autopct = valor" faz chamar a função valor que vai arredondar uma porcentagem para cada parte da pizza
	fig, ax = plt.subplots()
	ax.pie(x, labels = labels, autopct = valor)
	plt.savefig(pasta + '/resultados/votos.png')
	
	# Cria o arquivo "votos.txt" para salvar a contagem de votos
	
	t = 'Votos:<br>'
	for i in votos.keys():
		t += f"	{i}: {votos[i]}<br>"
	
	# Gera um html com a informaçao básica
	html = str()
	with open(pasta + "/templates/template.html", "r") as arq:
		html = arq.read()
	# ~ print(html)
	html = html.replace("{{texto}}", t)
	# ~ print(html)
	with open(pasta + "/resultados/votos.html", "w") as arq:
		arq.write(html)
	
	return 0

# e é uma porcentagem, mas ela vem quebrada. Esse programa arredonda para uma casa decimal
# essa função serve de callback para criar a função que cria a pizza
def valor(e):
	return f"{e:.1f}%"
	
main()

