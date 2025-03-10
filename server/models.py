from pydantic import BaseModel, Field
from typing import Optional, List

# Modelo de Usuário
class User(BaseModel):
    nome: str
    email: str
    idade: Optional[int] = None

# Modelo de Imóvel
class Imovel(BaseModel):
    titulo: str
    endereco: str
    cidade: str
    preco: float
    area: float
    quartos: int
    descricao: Optional[str] = None

# Modelo para receber previsões / análises (Ex.: IA)
class PredictRequest(BaseModel):
    area: float
    quartos: int
    cidade: str

# Modelo para resposta de análise
class PredictResponse(BaseModel):
    preco_estimado: float
    detalhe_analise: str
