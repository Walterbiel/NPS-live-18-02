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


#--------------------------------------

# Informações fixas sobre o que significa cada pergunta
st.write("### Descrição das perguntas de satisfação:")

st.write("""
**Q_um**: Nível de satisfação com a empresa (live18)  
**Q_dois**: Nível de satisfação com o tempo de entrega  
**Q_tres**: Nível de satisfação com o tempo de resposta aos pedidos  
**Q_quatro**: Nível de satisfação com o time de CX  
**Q_cinco**: Nível de satisfação com a qualidade do produto  
**Q_seis**: Nível de satisfação com a embalagem do produto  
**Q_sete**: Nível de satisfação com o preço  
**Q_oito**: Nível de satisfação com o aplicativo de status  
**Q_nove**: Nível de satisfação com a plataforma de pedidos  
""")


#--------------------------------------

st.title("Análise NPS Feedback")

# Gráfico de linhas - Quantidade de respostas por dia
st.subheader("Quantidade de Respostas ao Longo dos Dias")
fig, ax = plt.subplots(figsize=(10, 6))

# Contando o número de respostas por dia
respostas_por_dia = df.groupby('data_resposta').size().reset_index(name='quantidade_respostas')

# Plotando o gráfico de linhas
sns.lineplot(data=respostas_por_dia, x='data_resposta', y='quantidade_respostas', ax=ax, marker='o', color='b')

# Ajustando o gráfico
ax.set_title("Quantidade de Respostas ao Longo do Tempo")
ax.set_xlabel("Data de Resposta")
ax.set_ylabel("Quantidade de Respostas")
plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para melhor visualização
st.pyplot(fig)



# Criando subplots para cada pergunta (Q_um até Q_nove)
st.subheader("Distribuições de nota por questão")
fig, axes = plt.subplots(3, 3, figsize=(12, 10))  # 3 linhas, 3 colunas
fig.suptitle("Distribuição das Notas para Cada Pergunta", fontsize=16)

# Lista das colunas de perguntas
perguntas = ["Q_um", "Q_dois", "Q_tres", "Q_quatro", "Q_cinco", 
             "Q_seis", "Q_sete", "Q_oito", "Q_nove"]

# Criando os histogramas para cada pergunta
for i, col in enumerate(perguntas):
    ax = axes[i // 3, i % 3]  # Mapeia os subplots na grade 3x3
    sns.histplot(df[col], bins=10, kde=True, ax=ax, color="orange")
    ax.set_title(f"Distribuição - {col}")

# Ajustando layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Exibindo os gráficos no Streamlit
st.pyplot(fig)



# Gráfico de barras por estado
st.subheader("Classificação NPS por Estado")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df, x="estado", hue="classificacao_nps", ax=ax, palette="Set2")
ax.set_title("Distribuição da Classificação NPS por Estado")
ax.set_xlabel("Estado")
ax.set_ylabel("Contagem")
st.pyplot(fig)



# Gráfico de barras por mercado
st.subheader("Classificação NPS por Mercado")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df, x="mercado", hue="classificacao_nps", ax=ax, palette="Set2")
ax.set_title("Distribuição da Classificação NPS por Mercado")
ax.set_xlabel("Mercado")
ax.set_ylabel("Contagem")
st.pyplot(fig)



# Gráfico de barras por faixa etária
st.subheader("Classificação NPS por Faixa Etária")
# Definindo faixas etárias
bins = [0, 18, 30, 40, 50, 60, 100]
labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']
df['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels, right=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df, x="faixa_etaria", hue="classificacao_nps", ax=ax, palette="Set2")
ax.set_title("Distribuição da Classificação NPS por Faixa Etária")
ax.set_xlabel("Faixa Etária")
ax.set_ylabel("Contagem")
st.pyplot(fig)



# Calcular a média de cada pergunta Q_um até Q_nove
questions = ['Q_um', 'Q_dois', 'Q_tres', 'Q_quatro', 'Q_cinco', 'Q_seis', 'Q_sete', 'Q_oito', 'Q_nove']
mean_scores = df[questions].mean().sort_values()

# Selecionando as 3 perguntas com as notas mais baixas
lowest_questions = mean_scores.head(3)

# Exibir as 3 perguntas mais baixas no Streamlit
st.write("### 3 Perguntas com Notas Mais Baixas")
st.write(lowest_questions)

# Para cada uma das 3 perguntas mais baixas, verificar os estados e mercados
for question in lowest_questions.index:
    st.write(f"### Análise da Pergunta: {question}")
    
    # Filtrando os dados para a pergunta
    filtered_df = df[['estado', 'mercado', question]]
    
    # Agrupando por estado e mercado e calculando a média para cada uma
    state_market_avg = filtered_df.groupby(['estado', 'mercado'])[question].mean().reset_index()
    
    # Ordenando por nota para destacar as regiões mais críticas
    state_market_avg = state_market_avg.sort_values(by=question, ascending=True)
    
    # Gráfico de barras
    plt.figure(figsize=(12, 6))
    sns.barplot(data=state_market_avg, x='estado', y=question, hue='mercado', dodge=True)
    plt.title(f"Nota Média de {question} por Estado e Mercado")
    plt.xlabel("Estado")
    plt.ylabel(f"Nota Média de {question}")
    plt.xticks(rotation=45)
    
    # Exibindo o gráfico no Streamlit
    st.pyplot(plt)


