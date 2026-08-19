import os
from pathlib import Path
from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).resolve().parent
env_path = CURRENT_DIR.parent / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

DB_NAME = os.getenv("DB_NAME", "python_backend")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", 5432))
