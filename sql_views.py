import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do PostgreSQL no Docker
DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"  # Se estiver rodando no Docker, use "localhost" ou o nome do serviço no docker-compose
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando a engine do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição da view
views_sql = """
CREATE OR REPLACE VIEW nps_feedback_view AS 
SELECT 
    id,
    nome,
    idade,
    genero,
    estado,
    mercado,
    data_resposta,
    "Q_um",
    "Q_dois",
    "Q_tres",
    "Q_quatro",
    "Q_cinco",
    "Q_seis",
    "Q_sete",
    "Q_oito",
    "Q_nove",
    ROUND(
        ("Q_um" + "Q_dois" + "Q_tres" + "Q_quatro" + "Q_cinco" + "Q_seis" + "Q_sete" + "Q_oito" + "Q_nove") / 9.0
    ) AS media_final,
    CASE 
        WHEN ROUND(
            ("Q_um" + "Q_dois" + "Q_tres" + "Q_quatro" + "Q_cinco" + "Q_seis" + "Q_sete" + "Q_oito" + "Q_nove") / 9.0
        ) BETWEEN 1 AND 6 THEN 'Detrator'
        WHEN ROUND(
            ("Q_um" + "Q_dois" + "Q_tres" + "Q_quatro" + "Q_cinco" + "Q_seis" + "Q_sete" + "Q_oito" + "Q_nove") / 9.0
        ) BETWEEN 7 AND 8 THEN 'Neutro'
        WHEN ROUND(
            ("Q_um" + "Q_dois" + "Q_tres" + "Q_quatro" + "Q_cinco" + "Q_seis" + "Q_sete" + "Q_oito" + "Q_nove") / 9.0
        ) BETWEEN 9 AND 10 THEN 'Promotor'
    END AS classificacao_nps
FROM nps_feedback;
"""

# Criar a view no banco de dados
with engine.connect() as conn:
    conn.execute(text(views_sql))  # Executa a criação da view
    conn.commit()  # Confirma a alteração

print("View 'nps_feedback_view' criada/atualizada com sucesso!")
