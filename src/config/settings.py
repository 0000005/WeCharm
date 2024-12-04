import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Deepseek API configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Raise error if API key is not set
if not DEEPSEEK_API_KEY:
    raise ValueError(
        "DEEPSEEK_API_KEY environment variable is not set. Please set it in your .env file."
    )
