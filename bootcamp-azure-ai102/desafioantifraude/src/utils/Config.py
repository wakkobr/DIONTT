"""
Módulo de configuração do aplicativo.

Este módulo carrega as variáveis de ambiente necessárias para a execução do aplicativo,
incluindo as credenciais para o Azure Document Intelligence, Azure Blob Storage e o caminho do banco de dados.
"""

import os

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


class Config:
    """Classe para armazenar as configurações do aplicativo."""

    # Configurações para o Azure Document Intelligence
    AZURE_DOC_INT_ENDPOINT: str = os.getenv("AZURE_DOC_INT_ENDPOINT")
    """Endpoint do Azure Document Intelligence."""
    AZURE_DOC_INT_KEY: str = os.getenv("AZURE_DOC_INT_KEY")
    """Chave do Azure Document Intelligence."""

    # Configurações para o Azure Blob Storage
    AZURE_STORAGE_CONNECTION: str = os.getenv("AZURE_STORAGE_CONNECTION")
    """String de conexão do Azure Blob Storage."""
    CONTAINER_NAME: str = os.getenv("CONTAINER_NAME")
    """Nome do container no Azure Blob Storage."""

    # Configurações para o banco de dados SQLite
    DATABASE_PATH = "../data/credit_cards.db"
    """Caminho do arquivo do banco de dados SQLite."""

    # Validação das configurações
    @classmethod
    def validate_config(cls):
        """Valida se todas as configurações necessárias foram fornecidas."""
        required_vars = [
            "AZURE_DOC_INT_ENDPOINT",
            "AZURE_DOC_INT_KEY",
            "AZURE_STORAGE_CONNECTION",
            "CONTAINER_NAME",
        ]
        missing_vars = [var for var in required_vars if getattr(cls, var) is None]
        if missing_vars:
            raise ValueError(
                f"As seguintes variáveis de ambiente estão faltando: {', '.join(missing_vars)}"
            )


# Valida a configuração ao criar a classe
Config.validate_config()
