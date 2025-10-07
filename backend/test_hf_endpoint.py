"""
Teste para verificar o status dos endpoints Hugging Face.
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test_huggingface_endpoint():
    """Testa o endpoint do Hugging Face."""
    
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not token:
        print("❌ Token não encontrado")
        return
    
    endpoints = [
  
        "https://u9yyy2quq9hdyqbu.us-east-1.aws.endpoints.huggingface.cloud"
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    for endpoint in endpoints:
        print(f"\n🔍 Testando endpoint: {endpoint}")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Teste simples de GET
                response = await client.get(endpoint, headers=headers)
                print(f"  📊 GET Status: {response.status_code}")
                print(f"  📄 GET Response: {response.text[:200]}...")
                
                # Teste de POST com payload mínimo
                test_payload = {
                    "inputs": "Test",
                    "parameters": {
                        "max_new_tokens": 50,
                        "temperature": 0.1
                    }
                }
                
                response = await client.post(endpoint, headers=headers, json=test_payload)
                print(f"  📊 POST Status: {response.status_code}")
                print(f"  📄 POST Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"  ❌ Erro: {str(e)}")

if __name__ == "__main__":
    print("🧪 Teste de Endpoints Hugging Face")
    print("=" * 50)
    asyncio.run(test_huggingface_endpoint())