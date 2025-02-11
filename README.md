
### Análise NPS - Requerimentos dentro do arquivo pdf para mais detalhes

Instalar requeriments.txt para instalação de todos os pacotes necessários para utilizar os códigos:

$ pip install -r requirements.txt

Subir docker ou instalar manualmente o postgresSql:

$ docker-compose up -d

#### Subir API:

$ uvicorn event_producer:app --reload --port 8080

#### Chamar API: 

Método: POST
http://127.0.0.1:8080/gerar_dados/?num_rows=100

#### via cUrl:

curl -X 'POST' \
  'http://127.0.0.1:8080/gerar_dados/?num_rows=100' \
  -H 'accept: application/json'

Para documentação:
http://127.0.0.1:8080/docs