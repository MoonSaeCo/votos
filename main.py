import server
import setup
import contabilizar_votos
import os

class Tela():
	def __init__(self):
		self.menu = """################## Menu ##################
#                                        #
# 1 - Preparar Arquivos                  #
# 2 - Abrir Servidor                     #
# 3 - Contabilizar os votos              #
# 4 - Fechar                             #
#                                        #
##########################################
"""
	def opcoes(self):
		print(self.menu)
		opcao = input('> ')
		return opcao

def main():
	tela = Tela()
	opcao = "0"
	while opcao != "4":
		opcao = tela.opcoes()
		if opcao == "1":
			setup.main()
		if opcao == "2":
			try:
				os.system("python server.py")
			except:
				os.system("python3 server.py")
		if opcao == "3":
			contabilizar_votos.main()
	return 0

if __name__=="__main__":
	main()
