from urna import pasta_dados, n_pessoas
from json import load
from hashlib import sha256
from config import lista_canditados
import matplotlib.pyplot as plt

def main():
	votos = {}
	for i in lista_canditados:
		votos.update({i: 0})
	info = {}
	with open(pasta_dados + "info.json", 'r') as arq:
		info = load(arq)
	
	lista_pessoas = []
	
	for i in info["arquivos_pessoas"]:
		with open(pasta_dados + i['archive_name']) as arq:
			for j in arq.readlines():
				lista_pessoas.append(sha256(j.strip().encode()).hexdigest())
	
	
	for i in info['grupos']:
		with open(pasta_dados + i['archive_name']) as arq:
			for j in arq.readlines():
				l = j.strip().split(":")
				if l[1] in lista_pessoas:
					votos[l[0]] += 1
	# ~ print(f"Chapa 1: {votos['1']}\nChapa 2: {votos['2']}\nChapa 3: {votos['3']}\nChapa 4:{votos['4']}")
	
	labels = list()
	dic = dict()
	for i in votos.keys():
		labels.append(str(i))
		dic.update({str(i): votos[i]})
	x = list()
	for i in votos.keys():
		x.append(votos[i])
	
	
	fig, ax = plt.subplots()
	ax.pie(x, labels = labels, autopct = valor)
	# ~ y = 0
	# ~ for i in votos.keys():
		# ~ ax.text(-2.2, 1-(0.3 * y), f"{labels[y]}: {votos[i]}")
		# ~ y += 1
	# ~ ax.text(-1.7, , "oi")
	plt.savefig('votos.png')
	
	with open('votos.txt', 'w') as arq:
		arq.write('Votos:')
		for i in votos.keys():
			arq.write(f"	{i}: {votos[i]}\n")
	
	return 0

def valor(e):
	return f"{e:.1f}%"

