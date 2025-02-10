import pandas as pd
import numpy as np
from faker import Faker

# Inicializar Faker para gerar dados fictícios
fake = Faker()

# Definir número de linhas
num_rows = 1000

# Gerar dados fictícios
data = {
    "ID_Cliente": range(1, num_rows + 1),
    "Nome": [fake.name() for _ in range(num_rows)],
    "Email": [fake.email() for _ in range(num_rows)],
    "Idade": np.random.randint(18, 70, num_rows),
    "Gênero": np.random.choice(["Masculino", "Feminino"], num_rows),
    "Cidade": [fake.city() for _ in range(num_rows)],
    "País": [fake.country() for _ in range(num_rows)],
    "Pontuação_NPS": np.random.randint(0, 11, num_rows),
    "Categoria_NPS": np.random.choice(["Detrator", "Neutro", "Promotor"], num_rows, p=[0.3, 0.4, 0.3]),
    "Comentário_Produto": [fake.sentence() for _ in range(num_rows)],
    "Comentário_Atendimento": [fake.sentence() for _ in range(num_rows)],
    "Comentário_Preço": [fake.sentence() for _ in range(num_rows)],
    "Comentário_Entrega": [fake.sentence() for _ in range(num_rows)],
    "Comentário_Geral": [fake.paragraph() for _ in range(num_rows)],
    "Data_Resposta": [fake.date_this_year() for _ in range(num_rows)]
}

# Criar DataFrame
df_nps = pd.DataFrame(data)

# Exibir as primeiras linhas
df_nps.head()
