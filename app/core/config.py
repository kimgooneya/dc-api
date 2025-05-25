import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

# Load environment variables from .env file if it exists
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DC Inside Scraper API"
    
    # Cache settings
    CACHE_DURATION_MINUTES: int = int(os.getenv("CACHE_DURATION_MINUTES", 15))
    CACHE_DURATION: timedelta = timedelta(minutes=CACHE_DURATION_MINUTES)
    
    # DC Inside request settings
    DEFAULT_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    DC_BASE_URL: str = "https://gall.dcinside.com/mgallery/board/lists/"

settings = Settings() 