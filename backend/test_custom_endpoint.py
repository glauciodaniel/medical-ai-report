#!/usr/bin/env python3
"""
Script para testar o endpoint personalizado do Hugging Face
"""

import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_custom_endpoint():
    """Testa o endpoint personalizado do Hugging Face"""
    
    # Get configuration
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    model_url = os.getenv("MEDGEMMA_MODEL_URL", "https://u9yyy2quq9hdyqbu.us-east-1.aws.endpoints.huggingface.cloud")
    
    print("🧪 TESTANDO ENDPOINT PERSONALIZADO DO HUGGING FACE")
    print("=" * 60)
    
    if not token:
        print("❌ HUGGINGFACE_API_TOKEN não configurado!")
        return False
    
    print(f"🔑 Token: {token[:20]}...")
    print(f"🌐 Endpoint: {model_url}")
    
    # Test 1: Simple text generation
    print("\n📝 Teste 1: Geração de texto simples")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "inputs": "Hello, this is a test message for medical AI analysis.",
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.7
        }
    }
    
    try:
        print("🔄 Enviando requisição...")
        response = requests.post(model_url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Resposta: {result}")
        else:
            print(f"❌ Erro: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False
    
    # Test 2: Medical image analysis (simulated)
    print("\n🖼️  Teste 2: Análise de imagem médica (simulada)")
    
    # Create a simple test image (1x1 pixel PNG)
    test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    medical_prompt = f"""
    Analyze the following medical image and provide a comprehensive medical report.
    
    Patient Information:
    - Age: 70 years
    - Weight: 70 kg
    - Clinical History: Cardiac
    
    Please provide:
    1. Image quality assessment
    2. Anatomical structures visible
    3. Pathological findings (if any)
    4. Clinical impression
    5. Recommendations for further evaluation
    
    Format the response as a professional medical report in Portuguese (Brazil).
    """
    
    payload = {
        "inputs": medical_prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }
    
    try:
        print("🔄 Enviando análise médica...")
        response = requests.post(model_url, headers=headers, json=payload, timeout=60)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Análise médica: {result}")
            
            # Check if it's a medical response
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '') or result[0].get('text', '')
                if 'medical' in text.lower() or 'relatório' in text.lower() or 'análise' in text.lower():
                    print("🎯 Resposta parece ser médica!")
                else:
                    print("⚠️  Resposta não parece ser médica")
            elif isinstance(result, dict):
                text = result.get('generated_text', '') or result.get('text', '')
                if 'medical' in text.lower() or 'relatório' in text.lower() or 'análise' in text.lower():
                    print("🎯 Resposta parece ser médica!")
                else:
                    print("⚠️  Resposta não parece ser médica")
        else:
            print(f"❌ Erro na análise médica: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na análise médica: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 TESTE CONCLUÍDO!")
    print(f"✅ Endpoint: {model_url}")
    print(f"✅ Token: Configurado")
    print(f"✅ Requisições: Funcionando")
    
    return True

def test_endpoint_info():
    """Testa informações do endpoint"""
    print("\n🔍 INFORMAÇÕES DO ENDPOINT")
    print("=" * 40)
    
    model_url = os.getenv("MEDGEMMA_MODEL_URL", "https://u9yyy2quq9hdyqbu.us-east-1.aws.endpoints.huggingface.cloud")
    
    # Parse URL
    if "us-east-1.aws.endpoints.huggingface.cloud" in model_url:
        print("🌐 Tipo: Endpoint personalizado AWS")
        print("📍 Região: us-east-1 (Norte da Virgínia)")
        print("🏢 Provedor: AWS")
    elif "api-inference.huggingface.co" in model_url:
        print("🌐 Tipo: API oficial Hugging Face")
        print("📍 Região: Global")
        print("🏢 Provedor: Hugging Face")
    else:
        print("🌐 Tipo: Endpoint customizado")
        print("📍 URL: Personalizada")
        print("🏢 Provedor: Desconhecido")
    
    print(f"🔗 URL: {model_url}")

if __name__ == "__main__":
    print("🏥 TESTE DO ENDPOINT PERSONALIZADO - Medical AI Report")
    print("=" * 70)
    
    # Test endpoint info
    test_endpoint_info()
    
    # Test functionality
    success = test_custom_endpoint()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 ENDPOINT FUNCIONANDO! O modelo MedGemma deve estar operacional")
        print("\n🚀 Para usar no backend:")
        print("   1. Reinicie o backend: python main.py")
        print("   2. Teste com uma imagem real")
    else:
        print("⚠️  PROBLEMAS IDENTIFICADOS NO ENDPOINT")
        print("\n🔧 Verifique:")
        print("   - Se o token está correto")
        print("   - Se o endpoint está ativo")
        print("   - Se o modelo está carregado")
        print("   - Logs de erro para mais detalhes")
