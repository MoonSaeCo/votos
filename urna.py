import json
import os
from config import n_arquivos_pessoas as n_pessoas
from random import choice, randint
from hashlib import sha256
pasta_dados = os.path.join(os.getcwd() + '/dados/')

		

def escrever_voto(mat, voto):
	try:
		info = dict()
		with open(pasta_dados + 'info.json', 'r') as arq:
			info = json.load(arq)
		
		grupo = choice(info['not full'])
		pessoas = randint(0, n_pessoas - 1)
		
		archive_name = info['grupos'][grupo]['archive_name']
		info['grupos'][grupo]['n'] += 1
		info['arquivos_pessoas'][pessoas]['n'] += 1
		info['n_pessoas'] += 1
		
		if info['grupos'][grupo]['n'] == info['max_n']:
			info['not full'].pop(info['not full'].index(grupo))
		
		with open(pasta_dados + info['arquivos_pessoas'][pessoas]["archive_name"], 'a') as arq:
			arq.write(mat + "\n")
		
		with open(pasta_dados + f'grupo{grupo}.txt', 'a') as arq:
			mat_cript = sha256(mat.encode())
			arq.write(f'{voto}:{mat_cript.hexdigest()}\n')
		
		with open(pasta_dados + 'info.json', 'w') as arq:
			json.dump(info, arq, indent = 4)
		
		# ~ with open(pasta_dados + 'info.json', 'w') as  arq:
			# ~ json.dump(arq, info)
		return True
	except:
		return False
	
# ~ for k in range(100):
	# ~ x = str(randint(0, 9999))
	# ~ x = ("0" * (len(x) - 4)) + x
	# ~ escrever_voto(f'20253PEL{x}', '2')


