# Esse arquivo são as configurações do setup.py
#



n_grupos = 10
# Número de arquivos que serão gerados
# Os votos são distribuidos aleatoriamente pelos arquivos
# Assim mantém o voto secreto



max_n_grupo = 0
# Número maximo de pessoa por grupo, 0 para ilimitado
# Serve para evitar que um arquivo fique com mais pessoas que o outros
# Recomendado definir um limite caso o número de pessoas seja limitado



n_arquivos_pessoas = 3
# Número de arquivos que serão criados para salvar quem já votou
# Recomendado colocar mais de um 

lista_canditados = ['Chapa 1', 'Chapa 2', 'Chapa 3', 'Chapa 4']
# Uma lista usada para definir os candidatos que serão votados
# Precisa ser uma string
# Não colocar ';' nos nomes

necessidade_mesario = True
# Defina True ou False para a necessidade de ter um mesário para o voto ser realizado
