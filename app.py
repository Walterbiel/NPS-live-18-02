import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

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

