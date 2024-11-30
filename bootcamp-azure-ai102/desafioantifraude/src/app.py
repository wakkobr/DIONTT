import datetime

import pandas as pd
import requests
import streamlit as st
from services.blob_service import BlobStorageService
from services.credit_card_service import CreditCardValidator
from services.data_base import DatabaseService
from streamlit_lottie import st_lottie

# Inicialização de serviços globais
CREDIT_CARD_VALIDATOR = CreditCardValidator()
BLOB_STORAGE_SERVICE = BlobStorageService()
DATABASE_SERVICE = DatabaseService()


def carregar_lottie(url: str):
    """Carrega animação do Lottie Files."""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def render_sidebar():
    """
    Renderiza a barra lateral do aplicativo com navegação e informações do desenvolvedor.

    Returns:
        str: Página selecionada no menu
    """
    menu_options = {
        "Início": "🏠",
        "Análise de Cartão": "💳",
        "Consulta Banco de Dados": "🔍",
        "Documentação": "📚",
        "Sobre": "ℹ️",
    }

    selected_page = st.sidebar.radio(
        "Menu",
        list(menu_options.keys()),
        format_func=lambda x: f"{x} {menu_options[x]}",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👨‍💻 Desenvolvido por:\n**Julio Okuda**")

    st.sidebar.markdown(
        """
        <div class="social-links">
            <a href="https://github.com/Jcnok" target="_blank">
                <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />
            </a>
            <a href="https://linkedin.com/in/juliookuda" target="_blank">
                <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )

    return selected_page


def process_card_analysis(uploaded_file):
    """
    Processa a imagem de cartão de crédito carregada.

    Args:
        uploaded_file (UploadedFile): Arquivo de imagem carregado

    Returns:
        tuple: Informações do cartão e resultado da validação, ou None
    """
    try:
        st.image(uploaded_file, caption="Imagem do Cartão", use_column_width=True)

        with st.spinner("Processando..."):
            file_name = uploaded_file.name
            file = uploaded_file.getvalue()
            blob_url = BLOB_STORAGE_SERVICE.upload_blob(file, file_name)

            if not blob_url:
                st.error("Erro ao carregar imagem para o Blob Storage.")
                return None

            card_info = CREDIT_CARD_VALIDATOR.detect_credit_card_info_from_url(blob_url)
            if not card_info:
                st.error("Não foi possível analisar o cartão.")
                return None

            validation_result = CREDIT_CARD_VALIDATOR.validate_card_info(card_info)
            return card_info, validation_result

    except Exception as e:
        st.error(f"Erro durante análise do cartão: {e}")
        return None


def database_query_page():
    """
    Página de consulta ao banco de dados que exibe todos os dados automaticamente
    e permite executar queries personalizadas com exemplos prontos.
    """
    st.title("🔍 Consulta Banco de Dados")

    # Exibe automaticamente todos os dados ao carregar a página
    st.subheader("📊 Todos os Registros na Tabela `credit_cards`")
    try:
        all_data = DATABASE_SERVICE.get_all_cards()
        if all_data:
            df_all = pd.DataFrame(all_data)
            st.dataframe(df_all, use_container_width=True)

            # Botão para exportar todos os dados como CSV
            csv_all = df_all.to_csv(index=False)
            st.download_button(
                label="💾 Baixar Todos os Dados (CSV)",
                data=csv_all,
                file_name="todos_os_dados_credit_cards.csv",
                mime="text/csv",
            )
        else:
            st.info("⚠️ Nenhum dado encontrado na tabela `credit_cards`.")
    except Exception as e:
        st.error(f"Erro ao carregar todos os dados: {e}")

    # Permitir consultas personalizadas
    st.markdown("---")
    st.subheader("🔎 Consultas Personalizadas")
    st.markdown(
        """
        **Exemplos de Queries:**
        - Todos os registros: `SELECT * FROM credit_cards`
        - Cartões por id: `SELECT * FROM credit_cards WHERE id = 1`
        - Cartões por nome: `SELECT * FROM credit_cards WHERE card_name = "GABRIEL LIMA"`
        - Cartões emitidos pelo banco: `SELECT * FROM credit_cards WHERE bank_name = 'Banco X'`
        """
    )

    # Caixa de texto para consulta SQL
    query = st.text_area(
        "Digite sua consulta SQL:",
        placeholder="Exemplo: SELECT * FROM credit_cards WHERE bank_name = 'Banco X'",
        height=150,
    )

    if st.button("Executar Consulta"):
        try:
            # Executa a consulta personalizada
            results = DATABASE_SERVICE.execute_custom_query(query)

            if results:
                # Converte resultados para DataFrame
                df_results = pd.DataFrame(results)
                st.dataframe(df_results, use_container_width=True)

                # Botão para exportar os resultados como CSV
                csv_results = df_results.to_csv(index=False)
                st.download_button(
                    label="💾 Baixar Resultados (CSV)",
                    data=csv_results,
                    file_name="resultados_consulta.csv",
                    mime="text/csv",
                )
            else:
                st.info("🔍 Nenhum resultado encontrado para a consulta.")
        except ValueError as ve:
            st.error(f"❌ Erro de validação: {ve}")
        except Exception as e:
            st.error(f"❌ Erro ao executar a consulta: {e}")


def home_page():
    """
    Renderiza a página inicial com descrição do projeto.
    """
    st.title("🌟 Simplificando a Validação de Cartões no E-commerce")
    # Carregar animação
    lottie_translate = carregar_lottie(
        "https://lottie.host/c6d163ab-0ab8-49aa-8c50-332eb30e3774/kktucbjshh.json"
    )
    st_lottie(lottie_translate, height=300)
    st.markdown(
        """
      Já parou para pensar como algumas plataformas de e-commerce utilizam tecnologias
      avançadas para facilitar compras e prevenir fraudes? Lembra daquele momento mágico
      em que, ao finalizar uma compra, em vez de digitar todos os dados do cartão, você
      pode simplesmente enviar uma foto?
      #### 💡 Nossa Proposta
      Este projeto demonstra exatamente como essa mágica acontece! Utilizando a
      Inteligência Artificial da Azure, implementamos um sistema de validação
      de cartões que torna esse processo não só possível, mas também extremamente
      simples.
      #### 🚀 Como Funciona
      1. Faça upload da imagem do cartão
      2. A IA analisa os dados instantaneamente
      3. Receba a validação em segundos
      4. Dados são armazenados para análises futuras
      #### 🎯 Benefícios
      - Detecção automática das informações sem digitação
      - Interface intuitiva e amigável
      - Armazenamento para análises futuras
      - Consultas facilitadas com exportação para CSV
      #### 🔍 Explorando o Projeto
      Este é um projeto demonstrativo que utiliza tecnologias de ponta da Azure
      para mostrar como implementar validação de cartões de forma eficiente.
      Embora seja uma POC (Prova de Conceito), já inclui os principais elementos
      necessários para um sistema completo:
      - Extração precisa de dados do cartão
      - Validação em tempo real
      - Armazenamento estruturado
      - Interface para análise de dados
      #### 🎯 Objetivo
      Demonstrar na prática como as tecnologias modernas podem ser aplicadas
      para criar soluções que melhoram significativamente a experiência do
      usuário em transações financeiras.
    """
    )


def documentation_page():
    """
    Renderiza a página de documentação.
    """
    st.title("📚 Documentação")
    st.markdown(
        """
      # Documentação do Credit Card Analyzer

      ## Visão Geral

      Este aplicativo utiliza a API do Azure Document Intelligence para extrair informações de cartões de crédito a partir de imagens.  Os dados extraídos são então validados e persistidos em um banco de dados SQLite.

      ##  Funcionalidades Principais

      * **Upload de Imagem:** Permite ao usuário carregar uma imagem de um cartão de crédito.
      * **Análise de Imagem:** Usa a API do Azure Document Intelligence para detectar e extrair informações como número do cartão, data de validade, nome do titular e nome do banco.
      * **Validação de Cartão:** Realiza uma validação básica do número e data de validade do cartão.
      * **Armazenamento de Dados:** Armazena as informações do cartão (incluindo o resultado da validação) em um banco de dados SQLite.
      * **Consulta de Dados:** Permite consultar os dados armazenados no banco de dados utilizando consultas SQL.
      * **Exportação de Dados:** Permite exportar os resultados das consultas para um arquivo CSV.

      ##  Arquitetura

      O aplicativo segue uma arquitetura de três camadas:

      1. **Frontend (Streamlit):** Interface do usuário para interação com o usuário.
      2. **Backend (Python):** Lógica de negócio, incluindo a interação com os serviços da Azure e o banco de dados.
      3. **Azure Services:** Azure Document Intelligence e Azure Blob Storage.

      ##  Tecnologias Utilizadas

      * **Streamlit:** Framework Python para criar aplicações web.
      * **Python:** Linguagem de programação.
      * **Azure Document Intelligence:** Serviço da Azure para extração de informações de documentos.
      * **Azure Blob Storage:** Serviço da Azure para armazenamento de objetos de dados binários.
      * **SQLite:** Sistema de gerenciamento de banco de dados relacional.
    """
    )


def about_page():
    """
    Renderiza a página sobre o projeto.
    """
    st.title("ℹ️ Sobre")
    st.markdown(
        """
      ### 🎯 Projeto Credit Card Analyzer

      Este projeto é uma Prova de Conceito (POC) desenvolvida como parte do
      [Bootcamp Microsoft Certification Challenge #1 - AI 102](https://www.dio.me/bootcamp/microsoft-ai-102). O objetivo é demonstrar a aplicação
      prática de conceitos modernos de desenvolvimento e integração com
      serviços em nuvem da Azure.

      #### 🛠️ Tecnologias Utilizadas
      - **Frontend**: Streamlit
      - **Backend**: Python
      - **Cloud**: Azure Services
      - **Database**: SQLite
      - **Version Control**: Git

      #### 🌟 Características
      - Interface intuitiva
      - Processamento de imagem e validação
      - Armazenamento em banco de dados
      - Análise e exportação de dados
      - Integração com serviços Azure (Document Intelligence e Blob Storage)

      #### 👨‍💻 Desenvolvimento
      Desenvolvido por **Julio Okuda** como parte do projeto final do bootcamp,
      demonstrando a aplicação prática dos conceitos aprendidos durante o bootcamp.

      #### 📝 Nota
      Este é um projeto educacional e demonstrativo, não devendo ser utilizado
      em ambiente de produção sem as devidas adaptações e medidas de segurança.
    """
    )


def card_analysis_page():
    """
    Página para análise de cartões de crédito.
    """
    st.title("💳 Análise de Cartão")
    uploaded_file = st.file_uploader(
        "Carregue a imagem do cartão", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file and st.button("💳 Analisar Cartão"):
        result = process_card_analysis(uploaded_file)
        if result:
            card_info, validation_result = result

            st.write("Informações do Cartão:")
            st.write(card_info)

            if validation_result["is_valid"]:
                st.success("✅ Cartão Válido")
                existing_card = DATABASE_SERVICE.get_card_by_number(
                    card_info["card_number"]
                )

                if existing_card:
                    st.info(
                        f"Cartão já existe no banco de dados. ID: {existing_card['id']}"
                    )
                else:
                    card_info["is_valid"] = validation_result["is_valid"]
                    card_info["processed_at"] = datetime.datetime.now().isoformat()
                    DATABASE_SERVICE.insert_card(card_info)
                    st.success("Cartão inserido no banco de dados!")
            else:
                st.error("❌ Cartão Inválido")


def main():
    """
    Ponto de entrada para o aplicativo Credit Card Analyzer.
    """
    st.set_page_config(page_title="Credit Card Analyzer", page_icon="💳", layout="wide")

    # Mapeamento de páginas
    page_handlers = {
        "Início": home_page,
        "Análise de Cartão": card_analysis_page,
        "Consulta Banco de Dados": database_query_page,
        "Documentação": documentation_page,
        "Sobre": about_page,
    }

    # Renderiza a página selecionada
    selected_page = render_sidebar()
    handler = page_handlers.get(selected_page)

    if handler:
        handler()


if __name__ == "__main__":
    main()
