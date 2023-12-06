# GramaZen

## Descrição
Este repositório contem o código que abrange a prova de conceito desenvolvida para o contexto de outorga antecipada da disciplina de Projeto Integrador de Engenharias 2 da Universidade de Brasília.

O projeto consiste na emulação do funcionamento de um robô cortador de grama automatizado capaz de calcular, e recalcular, rotas para executar a poda de diferentes gramados.

A presente POC utiliza uma variação do algoritmo de DFS, considerando as necessidades intrínsecas à movimentação autônoma e ordenada do robô. O GIF abaixo apresenta um exemplo do funcionamento do algoritmo.

![Funcionamento do GramaZen - Visualização](/assets/GramaZen.gif)

## Como rodar o projeto

A execução do projeto ocorre de maneira bastante simplificada, basta seguir os passos a seguir:

1. Executar o comando `git clone` deste repositório
```
git clone https://github.com/KiSobral/GramaZen.git
```

2. (Opcional) No diretório do projeto, crie um ambiente virtual python para instalação das dependências. É possível criar um ambiente virtual python com o seguinte comando:
```
python3 -m venv venv
```
Uma vez criado o ambiente virtual, é preciso ativá-lo:
```
source venv/bin/activate # Para sistemas Unix

# OU

.\venv\Scripts\activate # Para sistemas Windows
```

3. No diretório do projeto, é preciso baixar as dependências do GramaZen por meio do comando:
```
pip3 install -r requirements.txt
```

4. Ainda no diretório do projeto, basta executar o arquivo principal de código, por meio do comando:
```
python3 src/main.py
```

Caso você receba algum erro de referência durante a execução do programa python, tente repetir o comando acima, porém localizado dentro da pasta `src/`.

```
cd src/
python3 main.py
```

## Funcionamento do projeto
### Comandos aceitos
- **Tecla "1"**: Insere o ponto de partida do cortador de grama onde está localizado o cursor do mouse. É necessário posicioná-lo antes de iniciar o processo de corte.
- **Tecla "q"**: Inicia o processo de corta da grama. Uma vez que ele é iniciado, não se pode mais inserir ou remover blocos.
- **Botão Esquerdo do Mouse**: Insere blocos de obstáculos no gramado. Ao manter o botão pressionado, bastar arrastar o mouse para inserir vários blocos.
- **Botão Direito do Mouse**: Remove quaisquer tipos de bloco do gramado. Ao manter o botão pressionado, basta arrastar o mouse para remover vários blocos.
- **Tecla "barra de espaço"**: Gera automaticamente um labirinto de obstáculos no gramado.
- **Tecla "x"**: Remove todos os blocos e informações do gramado.
- **Tecla "z"**: Remove apenas as informações da última poda do gramado, persistindo os blocos de obstáculos e ponto de partida.

### Dicionário de cores
- **Verde escuro**: Bloco de grama que ainda não foi cortado.    
- **Verde claro**:  Bloco de grama que já foi cortado.        
- **Branco**:       Bloco de grama ainda não cortado. Porém, já foi sensoreado anteriormente pelo cortador e está marcado para ser cortado.    
- **Azul claro**:   Representa a posição atual do cortador de grama.  
- **Preto**:        Representa blocos de obstáculos no gramado.  