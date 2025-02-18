import psycopg2
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração do PostgreSQL no Docker
DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_HOST = "localhost" 
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando a engine do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Nome da view criada no PostgreSQL
view_name = "nps_feedback_view"  # Substitua pelo nome correto da sua view

# Criando uma sessão no banco
with engine.connect() as conn:
    df = pd.read_sql(f"SELECT * FROM {view_name}", conn)

#-----------------------------------------------------------

# Dados de conexão (ajustado com o hostname correto)
host = "dpg-cupt48dumphs73eb1c50-a.oregon-postgres.render.com"
port = "5432"  # Porta padrão do PostgreSQL
dbname = "live_18_02_postgres_universidade"
user = "live_18_02_postgres_universidade_user"
password = "T14rPvIlLQfBUeAKQCh14vIaSUJgbWaD"

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Criando a engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

df.to_sql('nps_feedback', con=engine, if_exists='replace', index=False)

print("Dados enviados para a tabela com sucesso!")