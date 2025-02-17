# Análise NPS

Este projeto realiza uma análise de Net Promoter Score (NPS) com base em dados coletados de clientes. Para mais detalhes sobre os requerimentos, consulte o arquivo **.pdf** disponível no repositório.

## Dicionário de Dados

As perguntas e suas respectivas descrições:

- **Q_um**: Nível de satisfação com a empresa (live18)
- **Q_dois**: Nível de satisfação com o tempo de entrega
- **Q_tres**: Nível de satisfação com o tempo de resposta aos pedidos
- **Q_quatro**: Nível de satisfação com o time de CX
- **Q_cinco**: Nível de satisfação com a qualidade do produto
- **Q_seis**: Nível de satisfação com a embalagem do produto
- **Q_sete**: Nível de satisfação com o preço
- **Q_oito**: Nível de satisfação com o aplicativo de status
- **Q_nove**: Nível de satisfação com a plataforma de pedidos
- **Q_dez**: (Faltando descrição, adicionar)

## Cálculo do NPS

O NPS é calculado com base nas respostas dos clientes e categorizado da seguinte forma:

- **Detratores**: Notas de **1 a 6**
- **Neutros**: Notas de **7 a 8**
- **Promotores**: Notas de **9 a 10**

Fórmula:

\[ NPS = \frac{\text{Promotores} - \text{Detratores}}{\text{Número total de respondentes}} \]

## Instalação de Dependências

Para instalar os pacotes necessários, execute:

```bash
pip install -r requirements.txt
```

## Banco de Dados

Para utilizar o PostgreSQL, você pode:

### 1. Subir o banco via Docker:
```bash
docker-compose up -d
```

### 2. Ou instalar o PostgreSQL manualmente.

## Execução da API

Para iniciar a API, execute:

```bash
uvicorn event_producer:app --reload --port 8080
```

## Chamadas à API

### 1. Via HTTP (POST):

```plaintext
POST http://127.0.0.1:8080/gerar_dados/?num_rows=100
```

### 2. Via cURL:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8080/gerar_dados/?num_rows=100' \
  -H 'accept: application/json'
```

## Documentação

Para acessar a documentação interativa da API (Swagger UI), acesse:

[http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)



# 📊 API FastAPI para Geração de Dados Fictícios de NPS  

Este projeto implementa uma API utilizando **FastAPI** para gerar e armazenar dados fictícios de feedback NPS em um banco de dados **PostgreSQL**, usando **SQLAlchemy** como ORM e **Faker** para geração de dados sintéticos.  

## 📌 Tecnologias e Bibliotecas  

- **FastAPI** → Framework para criação de APIs REST de alto desempenho.  
- **SQLAlchemy** → ORM para definição do modelo de dados e interação com PostgreSQL.  
- **Faker** → Biblioteca para geração de dados fictícios realistas.  
- **NumPy** → Geração de valores aleatórios.  
- **Pandas** → Estruturação e manipulação de dados.  
- **Uvicorn** → Servidor ASGI para execução da API.  
- **PostgreSQL (via Docker)** → Banco de dados para persistência dos registros.  

## 📂 Estrutura e Funcionamento  

### 1️⃣ **Configuração da API**  

A API é criada utilizando **FastAPI**, com a seguinte configuração:  

```python
from fastapi import FastAPI

app = FastAPI()
```

Isso inicializa uma instância da aplicação, permitindo a definição de rotas e endpoints.  

---

### 2️⃣ **Configuração do Banco de Dados**  

A conexão com PostgreSQL é definida usando **SQLAlchemy**, configurando usuário, senha, host e porta:  

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://admin:admin123@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

Aqui, `create_engine()` inicializa a conexão, enquanto `sessionmaker()` permite a criação de sessões transacionais.  

---

### 3️⃣ **Definição do Modelo de Dados**  

O modelo `NPSFeedback` é definido como uma tabela SQLAlchemy, representando os campos necessários para armazenar os feedbacks:  

```python
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NPSFeedback(Base):
    __tablename__ = "nps_feedback"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    idade = Column(Integer)
    genero = Column(String)
    cidade = Column(String)
    pais = Column(String)
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
    Q_dez = Column(Integer)
```

A função `Base.metadata.create_all(bind=engine)` cria a tabela no banco caso ainda não exista.  

---

### 4️⃣ **Geração de Dados Fictícios**  

Os dados fictícios são criados com **Faker** e **NumPy**, gerando informações aleatórias para simular respostas de clientes:  

```python
from faker import Faker
import numpy as np

fake = Faker()

def generate_fake_data(num_rows=100):
    data = []
    for _ in range(num_rows):
        data.append({
            "nome": fake.name(),
            "idade": np.random.randint(18, 70),
            "genero": np.random.choice(["Masculino", "Feminino"]),
            "pais": fake.country(),
            "data_resposta": fake.date_this_year(),
            "mercado": np.random.choice([
                "Alimentos e Bebidas", "Tecnologia e Eletrônicos", "Saúde e Bem-Estar",
                "Moda e Vestuário", "Automotivo", "Educação e Treinamento",
                "Construção e Imobiliário", "Entretenimento e Mídia", "Beleza e Cosméticos", "Financeiro e Seguros"
            ]),
            "Q_um": np.random.randint(1, 10),
            "Q_dois": np.random.randint(1, 10),
            "Q_tres": np.random.randint(1, 10),
            "Q_quatro": np.random.randint(1, 10),
            "Q_cinco": np.random.randint(1, 10),
            "Q_seis": np.random.randint(1, 10),
            "Q_sete": np.random.randint(1, 10),
            "Q_oito": np.random.randint(1, 10),
            "Q_nove": np.random.randint(1, 10),
            "Q_dez": np.random.randint(1, 10)
        })
    return data
```

---

## 🚀 Como Rodar o Projeto  

### 1️⃣ Instalar Dependências  

```bash
pip install fastapi[all] pandas numpy faker sqlalchemy psycopg2
```

### 2️⃣ Configurar o PostgreSQL via Docker  

```bash
docker run --name postgres_nps -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres
```

### 3️⃣ Rodar a API  

```bash
uvicorn event_producer:app --reload --port 8080
```

### 4️⃣ Testar o Endpoint  

**Via requests:** 
```python
import requests

# URL da API
url = "http://127.0.0.1:8080/gerar_dados/"

# Parâmetro num_rows
params = {"num_rows": 2000}

# Enviar a requisição POST
response = requests.post(url, params=params)

# Verificar a resposta da API
if response.status_code == 200:
    print("Dados gerados com sucesso!")
    print(response.json()) 
else:
    print(f"Erro ao gerar dados. Status Code: {response.status_code}")
    print(response.text)

```

**Via Swagger UI:**  
- Acesse: [http://localhost:8080/docs](http://localhost:8080/docs)  

**Via cURL:**  
```bash
curl -X 'POST' 'http://localhost:8080/gerar_dados/?num_rows=200' -H 'accept: application/json'
```

### 5️⃣ Consultar Dados no PostgreSQL  

```sql
SELECT * FROM nps_feedback;
```

---


### Criar view no postgres, via Bash: 
```bash
python sql_views.py
```

### Para rodar o streamlit:
```bash
streamlit run app.py
```

