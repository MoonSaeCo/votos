import pickle as pkl
import json
import os
pasta_dados = 'dados/'

		

def escrever_voto(md, voto):
	info = dict()
	with open(pasta_dados + 'info.json', 'r') as arq:
		info = json.load(arq)
	
	
	
	x = info['current_cluster']
	if info['clusters'][x]['n'] < 100:
		arq_name = info['clusters'][x]['archive_name']
		info['clusters'][x]['n'] += 1
	else:
		new_cluster = {
			'id': x + 1,
			'archive_name': f'cluster{x + 1}.txt',
			'n': 1
		}
		arq_name = new_cluster['archive_name']
		info['clusters'].append(new_cluster)
		info['current_cluster'] = x + 1
	print(info)
	
		
	
	with open(pasta_dados + arq_name, 'a') as arq:
		arq.write(md)
		arq.write(voto)
	
	
	
	# ~ with open(pasta_dados + 'info.json', 'w') as  arq:
		# ~ json.dump(arq, info)
	
		

escrever_voto('a', '2')

