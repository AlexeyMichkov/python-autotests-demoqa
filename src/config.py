import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://demoqa.com")
    BOOKSTORE_URL: str = os.getenv("BOOKSTORE_URL", "https://demoqa.com/BookStore/v1")
    API_USER: str = os.getenv("API_USER", "")
    API_PASS: str = os.getenv("API_PASS", "")


config = Config()