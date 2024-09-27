from urna import pasta_dados, n_pessoas
from json import load
from hashlib import sha256
import matplotlib.pyplot as plt

def main():
	votos = {'1': 0, '2': 0, '3': 0, '4': 0}
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
					print(True, l[0])
				else:
					print(False, l[0])
	
	print(f"Chapa 1: {votos['1']}\nChapa 2: {votos['2']}\nChapa 3: {votos['3']}\nChapa 4:{votos['4']}")
	
	labels = list()
	dic = dict()
	for i in votos.keys():
		labels.append(f"Chapa {i}")
		dic.update({f"Chapa {i}": votos[i]})
	x = list()
	for i in votos.keys():
		x.append(votos[i])
	
	
	fig, ax = plt.subplots()
	ax.pie(x, labels = labels, autopct = valor)
	y = 1
	for i in votos.keys():
		print(y)
		ax.text(-2.2, 1.7-(0.3 * y), f"Chapa {y}: {votos[i]}")
		y += 1
	# ~ ax.text(-1.7, , "oi")
	plt.savefig('votos.png')
	return 0

def valor(e):
	return f"{e:.1f}%"

if __name__=="__main__":
	main()
