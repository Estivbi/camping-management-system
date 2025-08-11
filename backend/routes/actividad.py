from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Any, Optional
from models.actividad import (
    get_all_activities, 
    get_activity_by_id, 
    create_activity, 
    update_activity, 
    delete_activity,
    search_activities
)
from utils.auth import get_current_user
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter(prefix="/api/activities", tags=["activities"])

# Modelos Pydantic para validación
class ActivityCreate(BaseModel):
    name: str
    description: Optional[str] = None
    capacity: int
    price: Optional[Decimal] = None
    duration: Optional[int] = None
    is_active: bool = True

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    price: Optional[Decimal] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None

@router.get("/")
def get_activities(skip: int = 0, limit: int = 100):
    """Listar todas las actividades"""
    try:
        activities = get_all_activities(skip=skip, limit=limit)
        return activities  # Devolver directamente la lista, no envuelta en {"activities": ...}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo actividades: {str(e)}"
        )

@router.get("/search/{search_term}")
def search_activities_endpoint(search_term: str):
    """Buscar actividades por nombre o descripción"""
    try:
        activities = search_activities(search_term)
        return activities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error buscando actividades: {str(e)}"
        )

@router.get("/{activity_id}")
def get_activity(activity_id: int):
    """Obtener una actividad específica"""
    activity = get_activity_by_id(activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )
    return activity

@router.post("/")
def create_new_activity(activity: ActivityCreate, current_user: dict = Depends(get_current_user)):
    """Crear una nueva actividad"""
    try:
        activity_data = activity.model_dump()
        new_activity = create_activity(activity_data)
        return new_activity
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creando actividad: {str(e)}"
        )

@router.put("/{activity_id}")
def update_existing_activity(
    activity_id: int, 
    activity_update: ActivityUpdate, 
    current_user: dict = Depends(get_current_user)
):
    """Actualizar una actividad existente"""
    # Verificar que la actividad existe
    if not get_activity_by_id(activity_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )
    
    try:
        # Solo incluir campos que fueron proporcionados
        update_data = activity_update.model_dump(exclude_unset=True)
        updated_activity = update_activity(activity_id, update_data)
        
        if not updated_activity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo actualizar la actividad"
            )
        
        return updated_activity
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error actualizando actividad: {str(e)}"
        )

@router.delete("/{activity_id}")
def delete_existing_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Eliminar una actividad (soft delete)"""
    # Verificar que la actividad existe
    if not get_activity_by_id(activity_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )
    
    try:
        success = delete_activity(activity_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo eliminar la actividad"
            )
        
        return {"message": "Actividad eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error eliminando actividad: {str(e)}"
        )
