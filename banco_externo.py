import psycopg2

# Dados de conexão (ajustado com o hostname correto)
host = "dpg-cupt48dumphs73eb1c50-a.oregon-postgres.render.com"
port = "5432"  # Porta padrão do PostgreSQL
dbname = "live_18_02_postgres_universidade"
user = "live_18_02_postgres_universidade_user"
password = "T14rPvIlLQfBUeAKQCh14vIaSUJgbWaD"

# Conectar ao banco
try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

    cursor = connection.cursor()

    # Realizar operações no banco de dados
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("Conectado ao banco, versão:", db_version)

except Exception as e:
    print("Erro ao conectar ao banco:", e)

finally:
    if connection:
        cursor.close()
        connection.close()
