import streamlit as st
import requests
import json
import os

# Configuração da Página
st.set_page_config(page_title="JusCash - Analisador de Processos", page_icon="⚖️")

# Título e Descrição
st.title("⚖️ JusCash - Verificador de Elegibilidade")
st.markdown("Cole o JSON do processo judicial abaixo para verificar a conformidade com a Política de Compras.")

# Definição da URL da API
# Tenta pegar do Docker Compose, senão usa localhost (para testes fora do docker)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Área de Input
#JSON de exemplo para facilitar o teste
exemplo_json = {
  "numeroProcesso": "0023456-78.2022.4.05.0000",
  "classe": "Cumprimento de Sentença contra a Fazenda Pública",
  "orgaoJulgador": "VARA FEDERAL RECIFE/PE",
  "ultimaDistribuicao": "2024-08-12T09:30:00.000Z",
  "assunto": "Beneficio assistencial",
  "segredoJustica": false,
  "justicaGratuita": true,
  "siglaTribunal": "TRF5",
  "esfera": "Federal",
  "valorCondenacao": 50000.00,
  "documentos": [],
  "movimentos": []
}

json_input = st.text_area(
    "Dados do Processo (JSON)", 
    value=json.dumps(exemplo_json, indent=2), 
    height=300
)

# Botão de Ação
if st.button("Analisar Processo"):
    try:
        # 1. Tenta converter o texto para JSON
        dados_processo = json.loads(json_input)
        
        with st.spinner('Consultando o Oráculo Jurídico (LLM)...'):
            # 2. Envia para a API (Backend)
            response = requests.post(f"{API_URL}/analyze", json=dados_processo)
        
        # 3. Processa a resposta
        if response.status_code == 200:
            resultado = response.json()
            decisao = resultado.get("decision", "").lower()
            
            # Exibir Resultado Visualmente
            st.divider()
            st.subheader("Resultado da Análise")
            
            if decisao == "approved":
                st.success(f"✅ APROVADO")
            elif decisao == "rejected":
                st.error(f"❌ REPROVADO")
            elif decisao == "incomplete":
                st.warning(f"⚠️ INCOMPLETO")
            else:
                st.info(f"Decisão: {decisao}")
            
            # Exibir Justificativa e Citações
            st.markdown(f"**Justificativa:** {resultado.get('rationale')}")
            
            if resultado.get("citacoes"):
                st.markdown("**Regras Citadas:**")
                for regra in resultado.get("citacoes", []):
                    st.caption(f"• {regra}")
            
            # Debug: Mostrar JSON de resposta completo
            with st.expander("Ver JSON de Resposta Bruto"):
                st.json(resultado)
                
        else:
            st.error(f"Erro na API: {response.status_code}")
            st.text(response.text)

    except json.JSONDecodeError:
        st.error("O texto inserido não é um JSON válido. Por favor, verifique a formatação.")
    except requests.exceptions.ConnectionError:
        st.error("Não foi possível conectar à API.")