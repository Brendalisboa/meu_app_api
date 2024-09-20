from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto


class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    sku: str = "ABC12345"
    nome: str = "PORTA FRIOS"
    quantidade: Optional[int] = 62
    valor: float = 28.90


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no sku do produto.
    """
    sku: str = "ABC12345"


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "sku": produto.sku,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "valor": produto.valor,
        })

    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int = 1
    sku: str = "ABC12345"
    nome: str = "PORTA FRIOS"
    quantidade: Optional[int] = 12
    valor: float = 12.50


class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    sku: str

def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "sku": produto.sku,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "valor": produto.valor,
        
    }

class TotalProdutosSchema(BaseModel):
    total_produtos: int
    total_itens: int

class ErrorSchema(BaseModel):
    message: str
