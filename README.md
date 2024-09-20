# Minha API

API de Gerenciamento de Produtos

Esta API foi desenvolvida utilizando Flask e SQLAlchemy, com o suporte do Flask-OpenAPI para documentação automática. Ela permite o gerenciamento completo de produtos, incluindo a adição, visualização, remoção e busca de produtos armazenados em um banco de dados SQLite. A API também conta com a documentação automática via Swagger, Redoc, e RapiDoc, permitindo fácil visualização e interação com os endpoints.

Funcionalidades principais:
Adicionar produtos: Insere um novo produto na base de dados.
Listar todos os produtos: Retorna uma listagem de todos os produtos cadastrados.
Remover produto: Remove um produto específico da base de dados.
Obter totais: Retorna o número total de produtos cadastrados e a soma de todos os itens em estoque.


---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
