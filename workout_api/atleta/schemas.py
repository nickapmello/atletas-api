from typing import Optional
from pydantic import BaseModel, Field, PositiveFloat # type: ignore
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin

class CategoriaOut(BaseModel):
    nome: str

class CentroTreinamentoOut(BaseModel):
    nome: str

class Atleta(BaseSchema):
    nome: str = Field(description='Nome do atleta', example='Joao', max_length=50)
    cpf: str = Field(description='CPF do atleta', example='12345678900', max_length=11)
    idade: int = Field(description='Idade do atleta', example=25)
    peso: PositiveFloat = Field(description='Peso do atleta', example=75.5)
    altura: PositiveFloat = Field(description='Altura do atleta', example=1.70)
    sexo: str = Field(description='Sexo do atleta', example='M', max_length=1)
    categoria: CategoriaOut
    centro_treinamento: CentroTreinamentoOut

class AtletaIn(Atleta):
    categoria: CategoriaIn
    centro_treinamento: CentroTreinamentoAtleta

class AtletaOut(Atleta, OutMixin):
    categoria: CategoriaOut
    centro_treinamento: CentroTreinamentoOut

class AtletaUpdate(BaseSchema):
    nome: Optional[str] = Field(None, description='Nome do atleta', example='Joao', max_length=50)
    idade: Optional[int] = Field(None, description='Idade do atleta', example=25)
