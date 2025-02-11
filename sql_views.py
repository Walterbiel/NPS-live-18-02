import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do PostgreSQL no Docker
DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"  # Se estiver rodando no Docker, use "localhost" ou o nome do serviço no docker-compose
DB_PORT = "5432"
DB_NAME = "mydatabase"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando a engine do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição das views
views_sql = [
    # View para análise de NPS por categoria
    """
    CREATE OR REPLACE VIEW analise_nps_por_categoria AS
    SELECT 
        categoria_nps, 
        COUNT(*) AS total_respostas,
        ROUND(AVG(idade), 2) AS idade_media
    FROM nps_feedback
    GROUP BY categoria_nps;
    """,

    # View para análise de sentimentos nos comentários
    """
    CREATE OR REPLACE VIEW analise_sentimento_comentarios AS
    SELECT 
        cidade, 
        pais, 
        COUNT(comentario_produto) AS total_produto,
        COUNT(comentario_atendimento) AS total_atendimento,
        COUNT(comentario_preco) AS total_preco,
        COUNT(comentario_entrega) AS total_entrega,
        COUNT(comentario_geral) AS total_geral
    FROM nps_feedback
    GROUP BY cidade, pais;
    """,

    # View para análise temporal de NPS
    """
    CREATE OR REPLACE VIEW analise_nps_por_tempo AS
    SELECT 
        DATE_TRUNC('month', data_resposta) AS mes,
        categoria_nps,
        COUNT(*) AS total_respostas
    FROM nps_feedback
    GROUP BY mes, categoria_nps
    ORDER BY mes;
    """
]

# Criar as views no banco
with engine.connect() as conn:
    for view in views_sql:
        conn.execute(text(view))
    conn.commit()

print("View criada/atualizada com sucesso!")