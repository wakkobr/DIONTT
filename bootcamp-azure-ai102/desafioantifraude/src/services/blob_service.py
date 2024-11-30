"""Módulo para interação com o Azure Blob Storage."""

from azure.storage.blob import BlobServiceClient
from utils.Config import Config


class BlobStorageService:
    """Serviço para gerenciar o upload de arquivos para o Azure Blob Storage."""

    def __init__(self):
        """Inicializa o serviço com a string de conexão do Blob Storage."""
        self.blob_service_client = BlobServiceClient.from_connection_string(
            Config.AZURE_STORAGE_CONNECTION
        )

    def upload_blob(self, file_path: str, file_name: str) -> str:
        """Envia um arquivo para o Azure Blob Storage.

        Args:
            file_path: O caminho local do arquivo.
            file_name: O nome do arquivo a ser salvo no Blob Storage.

        Returns:
            A URL do arquivo no Blob Storage, ou None se ocorrer um erro.
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=Config.CONTAINER_NAME, blob=file_name
            )
            blob_client.upload_blob(file_path, overwrite=True)
            return blob_client.url
        except Exception as e:
            print(f"Erro no upload para Blob Storage: {e}")
            return None
