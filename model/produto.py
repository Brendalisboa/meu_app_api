from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Produto(Base):
    __tablename__ = 'produto'

    id = Column("pk_produto", Integer, primary_key=True)
    sku = Column(String(140), unique=True)
    nome = Column(String)
    quantidade = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, sku:str, nome:str, quantidade:int, valor:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            sku: sku do produto
            nome: descrição do produto
            quantidade: quantidade que se espera comprar daquele produto
            valor: valor esperado para o produto
            data_insercao: data de quando o produto foi inserido à base
        """
        self.sku = sku
        self.nome =nome
        self.quantidade = quantidade
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

   

