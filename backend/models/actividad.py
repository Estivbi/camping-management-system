from db import execute_query
from typing import Optional, List, Dict, Any

def get_all_activities(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Obtener todas las actividades"""
    query = """
    SELECT id, name, description, capacity, price, duration, location, 
           image_url, is_active, created_at
    FROM activities 
    WHERE is_active = true
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s;
    """
    return execute_query(query, (limit, skip), fetchall=True) or []

def get_activity_by_id(activity_id: int) -> Optional[Dict[str, Any]]:
    """Obtener una actividad por ID"""
    query = """
    SELECT id, name, description, capacity, price, duration, location, 
           image_url, is_active, created_at
    FROM activities 
    WHERE id = %s;
    """
    return execute_query(query, (activity_id,), fetchone=True)

def create_activity(activity_data: Dict[str, Any]) -> Dict[str, Any]:
    """Crear una nueva actividad"""
    query = """
    INSERT INTO activities (name, description, capacity, price, duration, location, image_url, is_active)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, name, description, capacity, price, duration, location, image_url, is_active, created_at;
    """
    
    params = (
        activity_data.get('name'),
        activity_data.get('description'),
        activity_data.get('capacity'),
        activity_data.get('price'),
        activity_data.get('duration'),
        activity_data.get('location'),
        activity_data.get('image_url'),
        activity_data.get('is_active', True)
    )
    
    return execute_query(query, params, fetchone=True)

def update_activity(activity_id: int, activity_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Actualizar una actividad existente"""
    # Construir la query dinámicamente basada en los campos proporcionados
    set_clauses = []
    params = []
    
    for field in ['name', 'description', 'capacity', 'price', 'duration', 'location', 'image_url', 'is_active']:
        if field in activity_data:
            set_clauses.append(f"{field} = %s")
            params.append(activity_data[field])
    
    if not set_clauses:
        return None
    
    params.append(activity_id)
    
    query = f"""
    UPDATE activities 
    SET {', '.join(set_clauses)}
    WHERE id = %s
    RETURNING id, name, description, capacity, price, duration, location, image_url, is_active, created_at;
    """
    
    return execute_query(query, params, fetchone=True)

def delete_activity(activity_id: int) -> bool:
    """Eliminar una actividad (soft delete - marcar como inactiva)"""
    query = """
    UPDATE activities 
    SET is_active = false 
    WHERE id = %s;
    """
    try:
        execute_query(query, (activity_id,))
        return True
    except Exception:
        return False

def search_activities(search_term: str) -> List[Dict[str, Any]]:
    """Buscar actividades por nombre o descripción"""
    query = """
    SELECT id, name, description, capacity, price, duration, location, 
           image_url, is_active, created_at
    FROM activities 
    WHERE is_active = true AND (
        name ILIKE %s OR description ILIKE %s
    )
    ORDER BY created_at DESC;
    """
    search_pattern = f"%{search_term}%"
    return execute_query(query, (search_pattern, search_pattern), fetchall=True) or []
