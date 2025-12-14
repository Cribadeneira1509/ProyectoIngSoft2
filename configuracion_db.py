import psycopg2

# --- Credenciales de Conexión Local ---
# Asegúrate de que estos valores coincidan con los de tu instalación de PostgreSQL
DB_HOST = "localhost"
DB_NAME = "sistema_reservas"
DB_USER = "postgres"
DB_PASSWORD = "12345" # <-- ¡Usa tu contraseña real de PostgreSQL!
DB_PORT = "5432" 

def conectar_db():
    """Establece y retorna una conexión a la base de datos."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"ERROR DE CONEXIÓN A POSTGRESQL: {e}")
        return None

def execute_query(query, params=None, fetch_data=False, fetch_all=False):
    """Función genérica para ejecutar consultas y manejar transacciones."""
    conn = conectar_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if fetch_data:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
            conn.commit() # Confirmar cambios para INSERT/UPDATE/DELETE
        
        cursor.close()
        return result
    except psycopg2.Error as e:
        print(f"Error de BD al ejecutar consulta: {e}")
        conn.rollback() # Revertir si hay error
        return None
    finally:
        if conn:
            conn.close()