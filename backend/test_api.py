#!/usr/bin/env python3
"""
Script de teste para a API do MedIA Reports
"""

import base64
import requests
import json
from PIL import Image
import io

def create_test_image():
    """Cria uma imagem de teste simples."""
    # Criar uma imagem simples de teste (100x100 pixels, branca)
    img = Image.new('RGB', (100, 100), color='white')
    
    # Converter para base64
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

def test_generate_report():
    """Testa o endpoint de geração de relatório."""
    
    # Dados de teste
    test_data = {
        "image": create_test_image(),
        "age": "45",
        "weight": "70",
        "clinical_history": "Paciente com dor torácica há 2 dias, sem fatores de risco cardiovascular conhecidos."
    }
    
    # URL do endpoint
    url = "http://localhost:8000/generate_report"
    
    try:
        print("🧪 Testando API do MedIA Reports...")
        print(f"📡 Enviando requisição para: {url}")
        
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sucesso! Relatório gerado:")
            print("="*60)
            print(result.get("report", "Erro: Campo 'report' não encontrado"))
            print("="*60)
            if result.get("message"):
                print(f"💬 Mensagem: {result['message']}")
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_health_endpoint():
    """Testa o endpoint de health."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        print("🏥 Health Check:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"❌ Erro no health check: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando testes da API MedIA Reports...\n")
    
    # Teste 1: Health check
    test_health_endpoint()
    print()
    
    # Teste 2: Geração de relatório
    test_generate_report()