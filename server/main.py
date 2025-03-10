from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd

# Importa MongoHandler e modelos Pydantic
from mongohandler import MongoHandler
from models import User, Imovel, PredictRequest, PredictResponse

# Instancia a aplicação FastAPI
app = FastAPI(
    title="API de Análise de Dados Imobiliários",
    description="Backend para gerenciar imóveis e usuários, além de endpoints para análises e IA.",
    version="1.0.0"
)

# Cria instância do nosso handler do Mongo
mongo_handler = MongoHandler()


# 1) Endpoint de teste e exemplo com Pandas
@app.get("/dataframe")
def get_dataframe_example():
    """
    Exemplo de retorno de dados em formato dataframe.
    """
    df = pd.DataFrame({
        "Nome": ["Alice", "Bob"],
        "Idade": [25, 30]
    })
    return df.to_dict(orient="records")


# 2) Endpoints para Usuários
@app.post("/users", response_description="Cria um novo usuário.")
async def create_user(user: User):
    inserted_id = await mongo_handler.insert("usuarios", user.dict())
    if not inserted_id:
        raise HTTPException(status_code=500, detail="Erro ao inserir usuário no MongoDB.")
    return {"message": "Usuário criado com sucesso!", "id": inserted_id}


@app.get("/users", response_description="Lista todos os usuários.")
async def list_users():
    data = await mongo_handler.find_all("usuarios", limit=1000)
    return data


@app.get("/users/{nome}", response_description="Busca usuários pelo nome.")
async def get_user_by_name(nome: str):
    data = await mongo_handler.find_by_field("usuarios", "nome", nome)
    if not data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return data


@app.put("/users/{nome}", response_description="Atualiza dados de um usuário pelo nome.")
async def update_user(nome: str, user: User):
    success = await mongo_handler.update_one("usuarios", "nome", nome, user.dict())
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao atualizar usuário.")
    return {"message": f"Usuário '{nome}' atualizado com sucesso."}


@app.delete("/users/{nome}", response_description="Deleta um usuário pelo nome.")
async def delete_user(nome: str):
    success = await mongo_handler.delete_one("usuarios", "nome", nome)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar usuário.")
    return {"message": f"Usuário '{nome}' deletado com sucesso."}


# 3) Endpoints para Imóveis
@app.post("/imoveis", response_description="Cadastra um novo imóvel.")
async def create_imovel(imovel: Imovel):
    inserted_id = await mongo_handler.insert("imoveis", imovel.dict())
    if not inserted_id:
        raise HTTPException(status_code=500, detail="Erro ao inserir imóvel no MongoDB.")
    return {"message": "Imóvel criado com sucesso!", "id": inserted_id}


@app.get("/imoveis", response_description="Lista todos os imóveis.")
async def list_imoveis():
    data = await mongo_handler.find_all("imoveis", limit=1000)
    return data


@app.get("/imoveis/{titulo}", response_description="Busca imóveis pelo título.")
async def get_imovel_by_title(titulo: str):
    data = await mongo_handler.find_by_field("imoveis", "titulo", titulo)
    if not data:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
    return data


@app.put("/imoveis/{titulo}", response_description="Atualiza dados de um imóvel pelo título.")
async def update_imovel(titulo: str, imovel: Imovel):
    success = await mongo_handler.update_one("imoveis", "titulo", titulo, imovel.dict())
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao atualizar imóvel.")
    return {"message": f"Imóvel '{titulo}' atualizado com sucesso."}


@app.delete("/imoveis/{titulo}", response_description="Deleta um imóvel pelo título.")
async def delete_imovel(titulo: str):
    success = await mongo_handler.delete_one("imoveis", "titulo", titulo)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar imóvel.")
    return {"message": f"Imóvel '{titulo}' deletado com sucesso."}


# 4) Endpoint de Análises/IA (exemplo simples)
@app.post("/prever", response_model=PredictResponse)
async def prever_imovel(req: PredictRequest):
    """
    Simulação de endpoint de IA que estima um preço com base em área, quartos e cidade.
    """
    # Exemplo: Modelagem simples (aleatória)
    import random

    preco_base = 1000.0 if req.cidade.lower() == "campinas" else 700.0
    preco_estimado = (req.area * preco_base) + (req.quartos * 2000) + random.uniform(0, 1000)
    detalhe = "Modelo de IA Fictício: base + area * factor + (quartos * 2000) + noise"

    return PredictResponse(
        preco_estimado=preco_estimado,
        detalhe_analise=detalhe
    )


# 5) Endpoint para testar conexão e listar coleções
@app.get("/mongo", response_description="Testa conexão Mongo e lista coleções.")
async def test_mongo_connection():
    try:
        collections = await mongo_handler.db.list_collection_names()
        return {"collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
