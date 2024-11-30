"""Módulo para interação com o banco de dados SQLite."""

import sqlite3
from typing import Dict, List, Optional

from utils.Config import Config


class DatabaseService:
    """Serviço para gerenciar o banco de dados SQLite."""

    def __init__(self):
        """Inicializa o serviço com o caminho do banco de dados."""
        self.db_path = Config.DATABASE_PATH
        self._create_table()

    def _create_table(self):
        """Cria a tabela credit_cards se ela não existir."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS credit_cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_name TEXT,
                    card_number TEXT,
                    expiry_date TEXT,
                    bank_name TEXT,
                    is_valid TEXT,
                    processed_at TEXT
                )
                """
            )
            conn.commit()

    def _execute_query(
        self, query: str, params: tuple = None
    ) -> Optional[sqlite3.Cursor]:
        """Executa uma query SQL com tratamento de erros.

        Args:
            query: A query SQL a ser executada.
            params: Os parâmetros da query (opcional).

        Returns:
            O cursor da query ou None caso ocorra um erro.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor
            except sqlite3.Error as e:
                print(f"Erro na execução do SQL: {e}")
                return None

    def insert_card(self, card_info: Dict[str, str]) -> int:
        """Insere informações de um cartão de crédito no banco de dados.

        Args:
            card_info: Um dicionário com as informações do cartão.

        Returns:
            O ID do cartão inserido, ou None se ocorrer um erro.
        """
        query = """
        INSERT INTO credit_cards (card_name, card_number, expiry_date, bank_name, is_valid, processed_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self._execute_query(
            query,
            (
                card_info["card_name"],
                card_info["card_number"],
                card_info["expiry_date"],
                card_info["bank_name"],
                card_info["is_valid"],
                card_info["processed_at"],
            ),
        )
        if cursor:
            return cursor.lastrowid
        return None

    def get_all_cards(self) -> List[Dict[str, str]]:
        """Retorna todas as informações dos cartões do banco de dados.

        Returns:
            Uma lista de dicionários, onde cada dicionário representa um cartão.
        """
        query = "SELECT * FROM credit_cards"
        cursor = self._execute_query(query)
        if cursor:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        return []

    def get_card_by_id(self, card_id: int) -> Optional[Dict[str, str]]:
        """Retorna um cartão específico."""
        query = "SELECT * FROM credit_cards WHERE id = ?"
        cursor = self._execute_query(query, (card_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None

    def get_card_by_number(self, card_number: int) -> Optional[Dict[str, str]]:
        """Retorna um cartão específico."""
        query = "SELECT * FROM credit_cards WHERE card_number = ?"
        cursor = self._execute_query(query, (card_number,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None

    def execute_custom_query(self, query: str) -> List[Dict[str, str]]:
        """Executa uma consulta SQL personalizada."""
        if query.lower().startswith(("select")):
            cursor = self._execute_query(query)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        else:
            raise ValueError("Apenas consultas SELECT são permitidas")

    def update_card(self, card_id: int, card_info: Dict[str, str]) -> bool:
        """Atualiza um cartão existente."""
        query = """
        UPDATE credit_cards
        SET card_name = ?, card_number = ?, expiry_date = ?,
            bank_name = ?, is_valid = ?, processed_at = ?
        WHERE id = ?
        """
        cursor = self._execute_query(
            query,
            (
                card_info["card_name"],
                card_info["card_number"],
                card_info["expiry_date"],
                card_info["bank_name"],
                card_info["is_valid"],
                card_info["processed_at"],
                card_id,
            ),
        )
        return cursor.rowcount > 0

    def delete_card(self, card_id: int) -> bool:
        """Deleta um cartão."""
        query = "DELETE FROM credit_cards WHERE id = ?"
        cursor = self._execute_query(query, (card_id,))
        return cursor.rowcount > 0
