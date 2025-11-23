# ⚖️ JusCash - Verificador de Processos Judiciais (AI-Powered)

Esta aplicação foi desenvolvida como parte do processo seletivo para a vaga de Analista de Machine Learning na JusCash. O objetivo é automatizar a análise de elegibilidade de processos judiciais utilizando **Large Language Models (LLMs)**.

## 📋 Visão Geral

O sistema recebe dados brutos de processos judiciais (JSON), analisa documentos e movimentos processuais usando o **Google Gemini 2.0 Flash**, e aplica a política de compras da JusCash para determinar se o ativo deve ser:
* ✅ **Approved** (Aprovado)
* ❌ **Rejected** (Reprovado)
* ⚠️ **Incomplete** (Incompleto)

## 📂 Estrutura do Projeto

```text
.
├── app
│   ├── api
│   │   └── main.py          # Backend: API FastAPI e Lógica do LLM
│   ├── frontend
│   │   └── ui.py            # Frontend: Interface Visual (Streamlit)
│   └── start.sh             # Script de inicialização dos serviços
├── docker-compose.yml       # Orquestração dos containers
├── Dockerfile               # Definição da imagem Docker
├── README.md                # Documentação (Este arquivo)
└── requirements.txt         # Dependências Python
``` 
## 🚀 Como Rodar Localmente (Docker)

### Pré-requisitos
* **Docker** e **Docker Compose** instalados.
* **Chave de API do Google** (Gemini).

### Passo a Passo

**1. Clone o repositório:**
```bash
git clone git@github.com:lPersonal-Projects/ML_JusCash.git
cd ML_JusCash
```

**2. Configure as Variáveis de Ambiente:**
Crie um arquivo `.env` na raiz do projeto e insira sua chave:

```env
GOOGLE_API_KEY=AIzaSy...
LANGCHAIN_API_KEY=lsv2_sk_7fafD....
# API_URL=http://api:8000 (Opcional, configurado automaticamente pelo Docker)
```

**3. Execute com Docker Compose:**
```bash
docker-compose up --build
```

**4. Acesse a Aplicação:**
* **Interface Visual (UI):** [http://localhost:8501](http://localhost:8501)
* **Documentação da API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

---

## 🔗 Endpoints da API

A API possui documentação interativa (OpenAPI/Swagger) no endpoint `/docs`.

### `POST /analyze`
Recebe o JSON do processo e retorna a decisão.

**Exemplo de Corpo da Requisição:**
```json
{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "classe": "Cumprimento de Sentença",
  "esfera": "Federal",
  "valorCondenacao": 50000,
  "documentos": [{"nome": "Certidão", "texto": "Trânsito em julgado certificado."}],
  "movimentos": [{"dataHora": "2024-01-01", "descricao": "Início da execução."}]
}
```

### `GET /health`
Endpoint de monitoramento para verificar se o serviço está online.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.11
* **Backend:** FastAPI (Alta performance e validação de dados)
* **LLM:** Google Gemini 2.0 Flash (Via LangChain)
* **Frontend:** Streamlit
* **Infraestrutura:** Docker & Docker Compose