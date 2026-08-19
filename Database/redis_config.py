import os
from pathlib import Path
from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).resolve().parent
env_path = CURRENT_DIR.parent / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

HOST = os.getenv("REDIS_HOST", "localhost")
PORT = int(os.getenv("REDIS_PORT", "6379"))
DECODE_RESPONSE = os.getenv("REDIS_DECODE_RESPONSE", "true").lower() == "true"
TTL = int(os.getenv("REDIS_TTL", "500"))