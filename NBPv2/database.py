from databases import Database
from sqlalchemy import create_engine, MetaData
from models import Base  # Importujemy Base z models.py, gdzie zdefiniowany jest model Currency

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/currency_db"

# Połączenie z bazą danych
database = Database(DATABASE_URL)

# Tworzymy silnik SQLAlchemy
engine = create_engine(DATABASE_URL)

# Tworzymy wszystkie tabele zdefiniowane w klasach ORM (w tym naszą tabelę "currencies")
Base.metadata.create_all(engine)