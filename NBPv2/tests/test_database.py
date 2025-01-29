import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.venv')))
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from main import database  # Załóżmy, że 'database' pochodzi z pliku main.py
from databases import Database

# Test połączenia z bazą danych
@pytest.mark.asyncio
async def test_database_connection():
    try:
        await database.connect()
        assert database.is_connected
    finally:
        await database.disconnect()

# Test zapytania do bazy danych
@pytest.mark.asyncio
async def test_fetch_currencies_from_db():
    await database.connect()  # Połączenie do bazy danych

    try:
        query = "SELECT * FROM currencies WHERE date = '2024-01-03'"
        result = await database.fetch_all(query)
        assert len(result) > 0
    finally:
        await database.disconnect()  # Rozłączenie po teście

