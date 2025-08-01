from db import execute_query

def create_user(username, email, password_hash):
    query = """
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
        RETURNING id, username, email, created_at;
    """
    return execute_query(query, (username, email, password_hash), fetchone=True)

def get_user_by_username(username):
    query = """
        SELECT id, username, email, password, created_at
        FROM users
        WHERE username = %s;
    """
    return execute_query(query, (username,), fetchone=True)
