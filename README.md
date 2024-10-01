# votos
> Sistema de votações sem fins lucrativos (até então)  construído para facilitar processos eleitorais, como do Grêmio ou Centro Acadêmico, dentro de instituições de ensino.

## Instalando dependências
```sh
pip install -r requirements.txt
```

## Executando o programa

- No terminal, dentro do diretório votos, coloque o comando:
    ```sh
    python3 main.py
    ```
    ou, dependendo da versão do python instalada:

    ```sh
    python main.py
    ``` 

## Dentro do main.py
### No programa surgirá 3 opções.
- Preparar arquivos
  - Irá deletar qualquer dado salvo e criará novos arquivos vazios.
- Abrir o servidor
  - Irá abrir o servidor. Para encerrar basta fazer ctrl + c
- Contabilizar votos
  - Irá criar um arquivo ("votos.png") com um gráfico pizza e um arquivo ("votos.txt") com os números de votos.
