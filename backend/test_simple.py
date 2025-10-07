"""
Teste simples para verificar a API.
"""

import requests
import json

def test_health_endpoint():
    """Testa o endpoint de saúde."""
    try:
        print("🏥 Testando endpoint /health...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Resposta: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")

def test_root_endpoint():
    """Testa o endpoint raiz."""
    try:
        print("\n🌐 Testando endpoint /...")
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Resposta: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")

def test_with_minimal_payload():
    """Testa com payload mínimo."""
    try:
        print("\n📝 Testando com payload mínimo...")
        payload = {
            "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",  # 1x1 pixel PNG em base64
            "age": "30",
            "weight": "70",
            "clinical_history": "Teste básico"
        }
        
        response = requests.post(
            "http://localhost:8000/generate_report",
            json=payload,
            timeout=10
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Success: {data.get('success')}")
            print(f"📋 Report length: {len(data.get('report', ''))}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")

if __name__ == "__main__":
    print("🧪 Teste Simples da API")
    print("=" * 40)
    
    test_root_endpoint()
    test_health_endpoint()
    test_with_minimal_payload()