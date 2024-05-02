from sqlite3 import IntegrityError
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status # type: ignore
from pydantic import UUID4 # type: ignore
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select # type: ignore

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo Centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    try:
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.dict())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.dict())
        
        db_session.add(centro_treinamento_model)
        await db_session.commit()
        return centro_treinamento_out
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Já existe um centro de treinamento cadastrado com este nome ou id."
        )

@router.get(
    '/', 
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=Page[CentroTreinamentoOut], # type: ignore
)
async def query(db_session: DatabaseDependency) -> Page[CentroTreinamentoOut]: # type: ignore
    centros_treinamento = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()
    return paginate([CentroTreinamentoOut.from_orm(centro) for centro in centros_treinamento]) # type: ignore

@router.get(
    '/{id}', 
    summary='Consulta um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Centro de treinamento não encontrado no id: {id}'
        )
    
    return CentroTreinamentoOut.from_orm(centro_treinamento)