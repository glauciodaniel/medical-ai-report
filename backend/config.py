import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Hugging Face API Configuration
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
MEDGEMMA_MODEL_URL = os.getenv("MEDGEMMA_MODEL_URL", "https://u9yyy2quq9hdyqbu.us-east-1.aws.endpoints.huggingface.cloud")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Model Configuration - Otimizado para MedGemma-4B-IT-YMF
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "32000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
TOP_P = float(os.getenv("TOP_P", "0.95"))

# Validation
def validate_config():
    """Validate that required configuration is present."""
    if not HUGGINGFACE_API_TOKEN:
        print("⚠️  AVISO: HUGGINGFACE_API_TOKEN não configurado!")
        print("   Para usar o modelo MedGemma, configure a variável de ambiente:")
        print("   export HUGGINGFACE_API_TOKEN='seu-token-aqui'")
        print("   Ou crie um arquivo .env na pasta backend/ com:")
        print("   HUGGINGFACE_API_TOKEN=seu-token-aqui")
        return False
    
    if not MEDGEMMA_MODEL_URL:
        print("⚠️  AVISO: MEDGEMMA_MODEL_URL não configurado!")
        print("   Configure a variável de ambiente MEDGEMMA_MODEL_URL")
        return False
    
    print(f"✅ Token configurado: {HUGGINGFACE_API_TOKEN[:10]}...")
    print(f"✅ Modelo configurado: {MEDGEMMA_MODEL_URL}")
    return True
