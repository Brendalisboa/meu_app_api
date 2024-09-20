from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func


from model import Session, Produto

from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização, remoção de produtos à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Rota para adicionar um novo produto à base de dados via requisição POST
@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados.

    Retorna uma representação dos produtos.
    """
    # Convertendo SKU para maiúsculas
    produto = Produto(
        sku=form.sku.upper(),
        nome=form.nome.upper(),
        quantidade=form.quantidade,
        valor=form.valor
    )
    
    logger.debug(f"Adicionando produto de sku: '{produto.sku}'")
    try:
        # criando conexão com a base
        session = Session()
        
        # Verificando se o SKU já existe (insensível a maiúsculas/minúsculas)
        existing_product = session.query(Produto).filter(func.lower(Produto.sku) == produto.sku.lower()).first()
        if existing_product:
            error_msg = "Produto de mesmo SKU já salvo na base."
            logger.warning(f"Erro ao adicionar produto '{produto.sku}', {error_msg}")
            return {"message": error_msg}, 409

        # Adicionando produto à base de dados
        session.add(produto)
        # Confirmando a transação
        session.commit()
        
        logger.debug(f"Adicionado produto de sku: '{produto.sku}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        session.rollback()  # Reverte transação em caso de erro
        error_msg = "Produto de mesmo SKU já salvo na base."
        logger.warning(f"Erro ao adicionar produto '{produto.sku}', {error_msg}. Detalhes: {str(e)}")
        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()  # Reverte qualquer transação em caso de erro inesperado
        error_msg = "Não foi possível salvar novo item."
        logger.warning(f"Erro ao adicionar produto '{produto.sku}', {error_msg}. Detalhes: {str(e)}")
        return {"message": error_msg}, 400

    finally:
        session.close()  # Fecha a sessão ao final, independentemente de erro ou sucesso


# Rota para buscar todos os produtos cadastrados
@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados.
    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()

    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


# Rota para deletar um produto a partir do SKU
@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do SKU.

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_sku = unquote(unquote(query.sku))
    print(produto_sku)
    logger.debug(f"Deletando dados sobre produto #{produto_sku}")
    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = session.query(Produto).filter(Produto.sku == produto_sku).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_sku}")
        return {"message": "Produto removido", "SKU": produto_sku}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{produto_sku}', {error_msg}")
        return {"message": error_msg}, 404


# Rota para retornar o número total de produtos cadastrados e a soma de todas as quantidades
@app.get('/produtos/total', tags=[produto_tag],
         responses={"200": TotalProdutosSchema, "404": ErrorSchema})
def get_total_produtos():
    """Retorna o número total de produtos cadastrados e a soma de todas as quantidades.

    Retorna a quantidade total de produtos e de itens no inventário.
    """
    logger.debug("Coletando total de produtos e itens")
    session = Session()

    try:
        # buscando a contagem de produtos e somando as quantidades
        total_produtos = session.query(func.count(Produto.id)).scalar()
        total_itens = session.query(func.sum(Produto.quantidade)).scalar()

        if total_produtos == 0:
            error_msg = "Nenhum produto encontrado."
            logger.warning(f"Erro ao buscar total de produtos, {error_msg}")
            return {"message": error_msg}, 404
        
        total_itens = total_itens if total_itens is not None else 0
        
        logger.debug(f"Total de produtos: {total_produtos}, Total de itens: {total_itens}")
        return {"total_produtos": total_produtos, "total_itens": total_itens}, 200

    except Exception as e:
        logger.error(f"Erro inesperado ao buscar totais: {str(e)}")
        return {"message": "Erro ao buscar totais de produtos"}, 500

    finally:
        session.close()
