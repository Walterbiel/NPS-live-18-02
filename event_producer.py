from fastapi import FastAPI, Query
import pandas as pd
import numpy as np
from faker import Faker

app = FastAPI()

# Inicializar Faker
fake = Faker()

# Definir número de linhas
total_rows = 1000

def generate_data(num_rows=total_rows):
    """ Gera dados fictícios de NPS."""
    return pd.DataFrame({
        "Nome": [fake.name() for _ in range(num_rows)],
        "Email": [fake.email() for _ in range(num_rows)],
        "Idade": np.random.randint(18, 70, num_rows),
        "Gênero": np.random.choice(["Masculino", "Feminino"], num_rows),
        "Cidade": [fake.city() for _ in range(num_rows)],
        "País": [fake.country() for _ in range(num_rows)],
        "Categoria_NPS": np.random.choice(["Detrator", "Neutro", "Promotor"], num_rows, p=[0.2, 0.4, 0.4]),
        "Comentário_Produto": [fake.sentence() for _ in range(num_rows)],
        "Comentário_Atendimento": [fake.sentence() for _ in range(num_rows)],
        "Comentário_Preço": [fake.sentence() for _ in range(num_rows)],
        "Comentário_Entrega": [fake.sentence() for _ in range(num_rows)],
        "Comentário_Geral": [fake.paragraph() for _ in range(num_rows)],
        "Data_Resposta": [fake.date_this_year() for _ in range(num_rows)]
    })

# Criar DataFrame com dados fictícios
df_nps = generate_data()

@app.get("/")
def home():
    return {"mensagem": "API de NPS funcionando!"}

@app.get("/dados")
def get_dados(categoria_nps: str = Query(None, description="Filtrar por categoria NPS (Detrator, Neutro, Promotor)")):
    """ Retorna os dados fictícios com filtro opcional por categoria NPS."""
    if categoria_nps:
        filtered_df = df_nps[df_nps["Categoria_NPS"] == categoria_nps]
    else:
        filtered_df = df_nps
    
    return filtered_df.to_dict(orient="records")
