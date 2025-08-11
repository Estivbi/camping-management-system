from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ActividadBase(BaseModel):
    name: str
    description: Optional[str] = None
    capacity: int
    price: Optional[Decimal] = None
    duration: Optional[int] = None  # en minutos
    location: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True

class ActividadCreate(ActividadBase):
    pass

class ActividadUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    price: Optional[Decimal] = None
    duration: Optional[int] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class Actividad(ActividadBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class ActividadResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    capacity: int
    price: Optional[Decimal] = None
    duration: Optional[int] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
