# votos
> Sistema de votações sem fins lucrativos (até então)  construído para facilitar processos eleitorais, como do Grêmio ou Centro Acadêmico, dentro de instituições de ensino.

## Instalando dependências
### Em "requirements.txt" temos os nomes das bibliotecas a serem instaladas.

    
    pip install flask
    
    
    pip install pyJWT
    
    
    pip install datetime

    
    pip install matplotlib
    
#### Este programa usa algumas bibliotecas teoricamente nativas, são as seguintes: "os", "hashlib" e "json'. Se alguma não estiver instalada, se certifique de instalar.
## Executando o programa

### No terminal, dentro do diretório votos, coloque o comando:
    
    python3 main.py
    
    ou, dependendo da versão do python instalada:

    
    python main.py 
    

## Dentro do main.py 
### No programa surgirá 3 opções.
- Preparar arquivos
  - Irá deletar qualquer dado salvo e criará novos arquivos vazios.
- Abrir o servidor
  - Irá abrir o servidor. Para encerrar basta fazer ctrl + c
- Contabilizar votos
  - Irá criar um arquivo ("votos.png") com um gráfico pizza e um arquivo ("votos.txt") com os números de votos.

## Contabilização de Votos
Quando rodar a contabilização de votos, os resultados vão aparecer na pasta resultados no arquivo votos.html
