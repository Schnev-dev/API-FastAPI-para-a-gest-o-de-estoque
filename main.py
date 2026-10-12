from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Literal

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./stockdb"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(
    title="API de Estoque",
    description="API para gerenciamento de estoque",
    version="1.0.0"
)


class ProdutoDB(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    nome = Column(String)
    quantidade = Column(Integer)
    limite_alerta = Column(Integer, default=3)

    def alerta_estoque(self):
        if self.quantidade <= self.limite_alerta:
            return "estoque baixo"
        return "estoque normal"

    # Alias para compatibilidade
    alerte_stock = alerta_estoque


class ProdutoCreate(BaseModel):
    sku: str = Field(..., description="Código SKU único do produto")
    nome: str = Field(..., description="Nome do produto")
    quantidade: int = Field(..., ge=0, description="Quantidade inicial em estoque")
    limite_alerta: int = Field(default=3, ge=0, description="Limite para alerta de estoque baixo")


Base.metadata.create_all(bind=engine)


def obter_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Alias para compatibilidade
session_db = obter_db


class AtualizarQuantidade(BaseModel):
    tipo: Literal["entrada", "saida"] = Field(..., description="Tipo de movimentação ('entrada' ou 'saida')")
    quantidade: int = Field(..., gt=0, description="Quantidade a adicionar ou retirar")


@app.get("/produtos/{id}", summary="Obter um produto")
def obter_produto(id: int, db=Depends(obter_db)):
    """Obtém os detalhes de um produto pelo seu ID."""
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    return {
        "id": produto.id,
        "sku": produto.sku,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "limite_alerta": produto.limite_alerta,
        "status": produto.alerta_estoque()
    }


# Alias para compatibilidade
obter_um_produto = obter_produto


@app.post("/produtos", summary="Adicionar um produto")
def adicionar_produto(produto: ProdutoCreate, db=Depends(obter_db)):
    """Cadastra um novo produto no estoque."""
    if db.query(ProdutoDB).filter(ProdutoDB.sku == produto.sku).first():
        raise HTTPException(status_code=400, detail=f"um produto com o SKU '{produto.sku}' já existe")
    db_produto = ProdutoDB(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


# Alias para compatibilidade
ajouter_produit = adicionar_produto


@app.post("/produtos/{id}/movimentos", summary="Registrar movimentação de estoque")
def registrar_movimento_produto(id: int, movimento: AtualizarQuantidade, db=Depends(obter_db)):
    """Registra uma entrada ou saída de estoque para um produto."""
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    if movimento.tipo == "entrada":
        produto.quantidade += movimento.quantidade
    elif movimento.tipo == "saida":
        if movimento.quantidade > produto.quantidade:
            raise HTTPException(status_code=400, detail="quantidade de saída superior ao estoque")
        produto.quantidade -= movimento.quantidade
    db.commit()
    db.refresh(produto)
    return {
        "id": produto.id,
        "sku": produto.sku,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "limite_alerta": produto.limite_alerta,
        "status": produto.alerta_estoque()
    }


# Alias para compatibilidade
mouvement_produit = registrar_movimento_produto


@app.get("/produtos", summary="Listar produtos")
def listar_produtos(
    estoque_baixo: bool = Query(False, description="Filtrar apenas produtos com estoque baixo"),
    db=Depends(obter_db)
):
    """Lista todos os produtos do estoque com opção de filtro para estoque baixo."""
    query = db.query(ProdutoDB)
    if estoque_baixo:
        query = query.filter(ProdutoDB.quantidade <= ProdutoDB.limite_alerta)
    produtos = query.all()
    return [
        {
            "id": produto.id,
            "sku": produto.sku,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "limite_alerta": produto.limite_alerta,
            "status": produto.alerta_estoque()
        }
        for produto in produtos
    ]


# Alias para compatibilidade
lister_produits = listar_produtos
