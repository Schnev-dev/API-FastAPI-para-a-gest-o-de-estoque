# API FastAPI para Gestão de Estoque

Projeto pessoal para praticar e demonstrar a criação de uma API REST com Python e FastAPI para gerenciamento de estoque.

## Visão geral

Esta aplicação permite registrar produtos, controlar entradas e saídas de estoque, consultar informações do inventário e identificar itens com nível crítico de quantidade. O projeto foi estruturado com foco em simplicidade, legibilidade e boas práticas para APIs modernas.

## Tecnologias

- Python 3.14+
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Funcionalidades

- Cadastro de produtos
- Consulta de produto por ID
- Listagem de todos os produtos
- Filtro por produtos com estoque baixo
- Registro de entrada e saída de itens
- Alertas automáticos de estoque
- Documentação interativa com Swagger

## Estrutura do projeto

```text
.
├── main.py
├── pyproject.toml
├── poetry.lock
├── stockdb
├── .gitignore
├── README.md
└── __pycache__/
```

## Pré-requisitos

- Python 3.14 ou superior
- Poetry

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Schnev-dev/API-FastAPI-para-a-gest-o-de-estoque.git
cd API-FastAPI-para-a-gest-o-de-estoque
```

2. Instale as dependências:

```bash
poetry install
```

3. Ative o ambiente virtual:

```bash
poetry shell
```

## Executando a API

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints principais

### 1. Obter produto por ID

```http
GET /produtos/{id}
```

### 2. Cadastrar produto

```http
POST /produtos
```

Exemplo de payload:

```json
{
  "sku": "SKU-001",
  "nome": "Café",
  "quantidade": 25,
  "limite_alerta": 5
}
```

### 3. Registrar movimentação de estoque

```http
POST /produtos/{id}/movimentos
```

Exemplo:

```json
{
  "tipo": "entrada",
  "quantidade": 10
}
```

ou

```json
{
  "tipo": "saida",
  "quantidade": 3
}
```

### 4. Listar produtos

```http
GET /produtos
```

Filtro opcional:

```http
GET /produtos?estoque_baixo=true
```

## Modelo de dados

Cada produto possui os seguintes campos:

- `id`
- `sku`
- `nome`
- `quantidade`
- `limite_alerta`

## Banco de dados

O projeto utiliza SQLite e cria o banco automaticamente ao iniciar a aplicação. O arquivo local é:

```text
stockdb
```

## Exemplo de resposta

```json
{
  "id": 1,
  "sku": "SKU-001",
  "nome": "Café",
  "quantidade": 18,
  "limite_alerta": 5,
  "status": "estoque baixo"
}
```

## Repositório

- GitHub: https://github.com/Schnev-dev/API-FastAPI-para-a-gest-o-de-estoque

## Autor

Schnev-dev

## Observações

Este projeto foi desenvolvido como uma aplicação prática de estudo e demonstração de habilidades em Python, APIs REST e integração com banco de dados relacional.
