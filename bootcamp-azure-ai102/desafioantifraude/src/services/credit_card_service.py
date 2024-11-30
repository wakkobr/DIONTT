"""Módulo para validação e processamento de informações de cartão de crédito."""

import re

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from utils.Config import Config


class CreditCardValidator:
    """Validador de informações de cartão de crédito usando Azure Document Intelligence."""

    def __init__(self):
        """Inicializa o validador com as credenciais da Azure."""
        self.credential = AzureKeyCredential(Config.AZURE_DOC_INT_KEY)
        self.document_client = DocumentIntelligenceClient(
            Config.AZURE_DOC_INT_ENDPOINT, self.credential
        )

    def _validate_card_number(self, card_number: str) -> bool:
        """Valida o formato do número do cartão de crédito.

        Args:
            card_number: O número do cartão de crédito.

        Returns:
            True se o número do cartão for válido, False caso contrário.
        """
        clean_card_number = card_number.replace(" ", "")
        return len(clean_card_number) >= 10 and clean_card_number.isdigit()

    def _validate_expiration_date(self, expiration_date: str) -> bool:
        """Valida o formato da data de expiração do cartão de crédito (MM/YY).

        Args:
            expiration_date: A data de expiração no formato MM/YY.

        Returns:
            True se a data de expiração for válida, False caso contrário.
        """
        pattern = r"^(0[1-9]|1[0-2])/\d{2}$"
        return bool(re.match(pattern, expiration_date))

    def validate_card_info(self, card_info: dict) -> dict:
        """Valida as informações do cartão de crédito.

        Args:
            card_info: Um dicionário contendo as informações do cartão.

        Returns:
            Um dicionário com o resultado da validação ('is_valid': True/False).
        """
        card_number = card_info.get("card_number", "").replace(" ", "")
        expiration_date = card_info.get("expiry_date", "")

        # Verifique se cada campo de informação foi encontrado e validado
        if not card_number or not expiration_date:
            print("Número do cartão ou data de expiração não fornecidos.")
            return {"is_valid": False}

        is_valid = all(
            [
                self._validate_card_number(card_number),
                self._validate_expiration_date(expiration_date),
            ]
        )
        return {"is_valid": is_valid}

    def detect_credit_card_info_from_url(self, card_url: str) -> dict:
        """Detecta informações do cartão de crédito a partir de uma URL da imagem.

        Args:
            card_url: A URL da imagem do cartão de crédito no Azure Blob Storage.

        Returns:
            Um dicionário contendo as informações do cartão detectadas, ou None se ocorrer um erro.
        """
        try:
            card_info = self.document_client.begin_analyze_document(
                "prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url)
            ).result()
            for document in card_info.documents:
                fields = document.fields
                return {
                    "card_name": fields.get("CardHolderName", {}).get("content", ""),
                    "card_number": fields.get("CardNumber", {})
                    .get("content", "")
                    .replace(" ", ""),
                    "expiry_date": fields.get("ExpirationDate", {}).get("content", ""),
                    "bank_name": fields.get("IssuingBank", {}).get("content", ""),
                }
            return None  # Nenhum documento encontrado
        except Exception as e:
            print(f"Erro na detecção de cartão: {e}")
            return None
