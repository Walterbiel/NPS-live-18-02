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
DB_HOST = "localhost"  # Se estiver rodando no Docker, use "localhost" ou o nome do serviço no docker-compose
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

st.title("Análise NPS")

# Exibir os dados como tabela no Streamlit
st.dataframe(df)

# Criar um gráfico de barras para visualizar a contagem de classificações NPS
st.subheader("Distribuição de Classificação NPS")
fig, ax = plt.subplots()
sns.countplot(x="classificacao_nps", data=df, palette="viridis", ax=ax)
st.pyplot(fig)
