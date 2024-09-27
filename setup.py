from config import *
import os
from json import dump, load

def main():
	print('Obtendo nome de arquivos')
	
	files_path = os.path.join(os.getcwd() + "/dados")
	l = os.listdir(files_path)
	
	print('Deletando Arquivos')
	
	for i in l:
		os.remove(files_path + f"/{i}")
		
	print('Arquivo Deletados')
	
	
	print('Criando info.json')
	info = {"grupos": [], "not full": [], "arquivos_pessoas": [], "max_n": max_n_grupo, "n_pessoas": 0}
	
	for i in range(0, n_grupos):
		info["grupos"].append({"archive_name": f"grupo{i}.txt", "n": 0})
		info["not full"].append(i)
		
	for i in range(0, n_arquivos_pessoas):
		info["arquivos_pessoas"].append({"archive_name": f"pessoas{i}.txt", "n": 0})
	
	with open(files_path + '/info.json', 'w') as arq:
		dump(info, arq, indent = 4)
	
	print('info.json criado')
	
	
	print('Criando arquivos de grupo')
	
	for i in range(0, n_grupos):
		with open(files_path + f"/grupo{i}.txt", "w") as arq:
			pass
	
	print('Arquivos de grupo criados')
	
	
	print('Criando arquivos de pessoas')
	
	for i in range(0, n_arquivos_pessoas):
		with open(files_path + f"/pessoas{i}.txt", "w") as arq:
			pass
	
	print('Arquivos de pessoas criados')
	return 0


if __name__ == "__main__":
	main()
