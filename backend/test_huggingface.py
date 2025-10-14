#!/usr/bin/env python3
"""
Script de teste para verificar a conectividade com a API do Hugging Face
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_huggingface_connection():
    """Testa a conexão com a API do Hugging Face"""
    
    # Get token and model URL from environment
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    model_url = os.getenv("MEDGEMMA_MODEL_URL", "https://api-inference.huggingface.co/models/google/medgemma-2b")
    
    if not token or token == "your-huggingface-api-token-here":
        print("❌ ERRO: HUGGINGFACE_API_TOKEN não configurado!")
        print("Configure a variável de ambiente ou crie um arquivo .env")
        return False
    
    print(f"🔑 Token encontrado: {token[:10]}...")
    print(f"🌐 Modelo: {model_url}")
    
    # Test API endpoint
    headers = {"Authorization": f"Bearer {token}"}
    
    # Simple test payload
    payload = {
        "inputs": "Hello, this is a test message.",
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.7
        }
    }
    
    try:
        print("🔄 Testando conexão com a API do Hugging Face...")
        response = requests.post(model_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("✅ Conexão bem-sucedida!")
            result = response.json()
            print(f"📝 Resposta: {result}")
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_image_processing():
    """Testa o processamento de imagem (requer token válido)"""
    
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    model_url = os.getenv("MEDGEMMA_MODEL_URL", "https://api-inference.huggingface.co/models/google/medgemma-2b")
    
    if not token or token == "your-huggingface-api-token-here":
        print("⚠️  Pule o teste de imagem - token não configurado")
        return False
    
    # Create a simple test image (1x1 pixel PNG)
    import base64
    test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "inputs": f"Analyze this medical image: {test_image}",
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }
    
    try:
        print("🖼️  Testando processamento de imagem...")
        response = requests.post(model_url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            print("✅ Processamento de imagem bem-sucedido!")
            return True
        else:
            print(f"❌ Erro no processamento: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de imagem: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testando configuração do Hugging Face...")
    print("=" * 50)
    
    # Test basic connection
    connection_ok = test_huggingface_connection()
    
    if connection_ok:
        print("\n" + "=" * 50)
        # Test image processing
        test_image_processing()
    
    print("\n" + "=" * 50)
    if connection_ok:
        print("🎉 Configuração do Hugging Face está funcionando!")
        print("Você pode executar o backend com: python main.py")
    else:
        print("⚠️  Configure o HUGGINGFACE_API_TOKEN antes de executar o backend")
        print("Crie um arquivo .env na pasta backend/ com:")
        print("HUGGINGFACE_API_TOKEN=seu-token-aqui")
