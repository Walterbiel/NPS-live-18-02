from fastapi import FastAPI
import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

# Criando a aplicação FastAPI
app = FastAPI()

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

# Definição da tabela no SQLAlchemy
class NPSFeedback(Base):
    __tablename__ = "nps_feedback"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    idade = Column(Integer)
    genero = Column(String)
    estado = Column(String)
    mercado = Column(String)
    data_resposta = Column(Date)
    Q_um = Column(Integer)
    Q_dois = Column(Integer)
    Q_tres = Column(Integer)
    Q_quatro = Column(Integer)
    Q_cinco = Column(Integer)
    Q_seis = Column(Integer)
    Q_sete = Column(Integer)
    Q_oito = Column(Integer)
    Q_nove = Column(Integer)

# Criando a tabela no banco (caso ainda não exista)
Base.metadata.create_all(bind=engine)

# Inicializando o Faker
fake = Faker()

estados_brasil = [
    "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
    "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
    "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí",
    "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
    "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
]

# Definir probabilidades para cada valor de 1 a 10
probabilidades = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.3, 0.2, 0.2]

# Função para gerar dados fictícios
def generate_fake_data(num_rows=100):
    data = []
    for _ in range(num_rows):
        data.append({
            "nome": fake.name(),
            "idade": np.random.randint(18, 70),
            "genero": np.random.choice(["Masculino", "Feminino"]),
            "estado": np.random.choice(estados_brasil),
            "data_resposta": fake.date_this_year(),
            "mercado": np.random.choice(["Alimentos e Bebidas", "Tecnologia e Eletrônicos", "Saúde e Bem-Estar", "Moda e Vestuário", "Automotivo", "Educação e Treinamento", "Construção e Imobiliário", "Entretenimento e Mídia", "Beleza e Cosméticos", "Financeiro e Seguros"]),
            "Q_um": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades),
            "Q_dois": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades),
            "Q_tres": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades),
            "Q_quatro": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades),
            "Q_cinco": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades),
            "Q_seis": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades),
            "Q_sete": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades),
            "Q_oito": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades),
            "Q_nove": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=probabilidades)
        })
    return data

# Rota para gerar e armazenar os dados no PostgreSQL
#Metódo POST
@app.post("/gerar_dados/")
def gerar_dados(num_rows: int = 100):
    fake_data = generate_fake_data(num_rows)
    
    # Criando uma sessão do banco de dados
    db = SessionLocal()
    
    # Convertendo os dados para objetos SQLAlchemy
    db_records = [NPSFeedback(**row) for row in fake_data]

    # Inserindo no banco de dados
    db.add_all(db_records)
    db.commit()
    db.close()

    return {"message": f"{num_rows} registros inseridos com sucesso no PostgreSQL!"}
