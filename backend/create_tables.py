#!/usr/bin/env python3
"""
Script para crear la tabla de actividades en PostgreSQL
"""
from db import execute_query

def create_activities_table():
    """Crear la tabla de actividades"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS activities (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        capacity INTEGER NOT NULL,
        price DECIMAL(10,2),
        duration INTEGER, -- en minutos
        location VARCHAR(100),
        image_url VARCHAR(255),
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        execute_query(create_table_query)
        print("✅ Tabla 'activities' creada exitosamente!")
    except Exception as e:
        print(f"❌ Error creando tabla 'activities': {e}")

def insert_sample_activities():
    """Insertar algunas actividades de ejemplo"""
    sample_activities = [
        ("Senderismo en el Bosque", "Caminata guiada por los senderos naturales del camping", 15, 25.00, 120, "Bosque Norte", "https://example.com/hiking.jpg", True),
        ("Taller de Artesanía", "Aprende a crear objetos decorativos con materiales naturales", 8, 15.00, 90, "Sala de Actividades", "https://example.com/craft.jpg", True),
        ("Observación de Aves", "Actividad matutina para observar la fauna local", 10, 20.00, 150, "Mirador del Lago", "https://example.com/birds.jpg", True),
        ("Fogata Nocturna", "Velada nocturna con canciones y historias alrededor del fuego", 25, 5.00, 120, "Área de Fogata", "https://example.com/campfire.jpg", True),
        ("Kayak en el Lago", "Paseo en kayak por las aguas cristalinas del lago", 6, 40.00, 180, "Embarcadero", "https://example.com/kayak.jpg", True)
    ]
    
    insert_query = """
    INSERT INTO activities (name, description, capacity, price, duration, location, image_url, is_active)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    try:
        for activity in sample_activities:
            execute_query(insert_query, activity)
        print("✅ Actividades de ejemplo insertadas exitosamente!")
    except Exception as e:
        print(f"❌ Error insertando actividades de ejemplo: {e}")

if __name__ == "__main__":
    create_activities_table()
    insert_sample_activities()
