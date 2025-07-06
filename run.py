# run.py
from app import app
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    app.run(
        debug=os.getenv("DEBUG", "False").lower() in ("true", "1", "t"),
        host="0.0.0.0",
        port=5000,
    )