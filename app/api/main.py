import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Importações do LangChain (Garanta que instalou: langchain, langchain-openai)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Carregar variáveis de ambiente (.env)
load_dotenv()

# --- 1. Definição dos Modelos de Dados (Pydantic) ---
class Documento(BaseModel):
    id: str
    dataHoraJuntada: Optional[str] = None
    nome: str
    texto: Optional[str] = ""

class Movimento(BaseModel):
    dataHora: str
    descricao: str

class Honorarios(BaseModel):
    contratuais: Optional[float] = 0.0
    periciais: Optional[float] = 0.0
    sucumbenciais: Optional[float] = 0.0

class Processo(BaseModel):
    numeroProcesso: str
    classe: str
    orgaoJulgador: Optional[str] = None
    ultimaDistribuicao: Optional[str] = None
    valorCausa: Optional[float] = 0.0
    assunto: Optional[str] = None
    segredoJustica: bool = False
    justicaGratuita: bool = False
    siglaTribunal: str
    esfera: str  # Importante para POL-4
    valorCondenacao: Optional[float] = None # Importante para POL-2 e POL-3
    documentos: List[Documento] = []
    movimentos: List[Movimento] = []
    honorarios: Optional[Honorarios] = None

# Modelo de Saída (Output esperado pelo Case)
class AnaliseOutput(BaseModel):
    decision: str = Field(description="approved, rejected ou incomplete")
    rationale: str = Field(description="Justificativa clara da decisão")
    citacoes: List[str] = Field(description="Lista de regras citadas, ex: ['POL-1']")

# --- 2. Configuração da API ---

app = FastAPI(
    title="JusCash AI Analyzer",
    description="API para análise automatizada de processos judiciais usando LLM.",
    version="1.0.0"
)

# --- 3. Engenharia de Prompt e LLM ---

def get_llm_chain():
    # Configura o modelo Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        max_retries=2,
    )
    
    # Definição das Regras de Negócio
    politica_juscash = """
    Você é um analista jurídico sênior. Sua tarefa é analisar dados JSON de processos judiciais.
    
    Siga ESTRITAMENTE estas regras (Policies):
    
    CRITÉRIOS DE ELEGIBILIDADE (Regra Base):
    - POL-1: O processo DEVE estar "Transitado em Julgado" E em "Fase de Execução" (cumprimento de sentença iniciado, RPV expedido, etc).
    - POL-2: O valor da condenação deve ser maior que zero.

    CRITÉRIOS DE REJEIÇÃO:
    - POL-3: Valor da condenação menor que R$ 1.000,00.
    - POL-4: Esfera "Trabalhista".
    - POL-5: Óbito do autor sem inventário.
    - POL-6: Substabelecimento sem reserva de poderes.

    CRITÉRIOS DE DADOS INCOMPLETOS:
    - POL-8: Falta documento essencial para provar o Trânsito em Julgado ou a Fase de Execução.

    FORMATO DE RESPOSTA (JSON):
    {{
        "decision": "approved" | "rejected" | "incomplete",
        "rationale": "Explicação curta e direta citando o motivo.",
        "citacoes": ["POL-X"]
    }}
    """
    
    # O restante continua igual...
    prompt = ChatPromptTemplate.from_messages([
        ("system", politica_juscash),
        ("human", "Analise este processo:\n{input_json}")
    ])

    parser = JsonOutputParser(pydantic_object=AnaliseOutput)

    chain = prompt | llm | parser
    return chain

# --- 4. Endpoints da API ---

@app.get("/health")
def health_check():
    """Endpoint obrigatório de saúde."""
    return {"status": "ok", "service": "JusCash-Analyzer"}

@app.post("/analyze", response_model=AnaliseOutput)
async def analyze_lawsuit(processo: Processo):
    """
    Recebe os dados do processo, valida com Pydantic e envia para o LLM.
    """
    try:
        # Converter o objeto Pydantic para JSON string para passar ao prompt
        processo_dict = processo.model_dump()
        processo_json = json.dumps(processo_dict, ensure_ascii=False, indent=2)
        
        # Invocar a cadeia do LangChain
        chain = get_llm_chain()
        resultado = chain.invoke({"input_json": processo_json})
        
        return resultado

    except Exception as e:
        # Log do erro (útil para observabilidade)
        print(f"Erro na análise: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Para rodar localmente sem Docker (opcional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)