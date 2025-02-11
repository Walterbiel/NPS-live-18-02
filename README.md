### Análise NPS - Requerimentos dentro do arquivo pdf para mais detalhes

#### Dicionario de dados:
Q_um = Nível de satisfação com a empresa_live18

Q_dois = Nível de satisfação com o tempo de entrega

Q_tres = Nível de satisfação com o tempo de resposta aos pedidos

Q_quatro = Nível de satisfação com o time de CX

Q_cinco = Nível de satisfação com a qualidade do produto

Q_seis = Nível de satisfação com a embalagem do produo

Q_sete = Nível de satisfação com a 

Q_oito = Nível de satisfação com a 

Q_nove = Nível de satisfação com a 

Q_dez =Nível de satisfação com a 

#### Cálculo NPS:
Detrator: 1-6 ; Neutro: 7-8 ; Promotor: 9-10

NPS=(Promotores-Detratores)/Númerototalderespondentes           


#### Instalar requeriments.txt para instalação de todos os pacotes necessários para utilizar os códigos:

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