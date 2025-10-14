"""
Teste para verificar se a imagem está sendo enviada corretamente.
"""

import base64
import io
from PIL import Image
import requests
import json

def create_test_image():
    """Cria uma imagem de teste simples."""
    # Cria uma imagem RGB simples
    img = Image.new('RGB', (200, 200), color='red')
    
    # Converte para base64
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return img_base64

def test_image_upload():
    """Testa o upload da imagem para a API."""
    
    # Criar imagem de teste
    test_image = create_test_image()
    print(f"✅ Imagem de teste criada com tamanho: {len(test_image)} caracteres")
    
    # Dados de teste
    payload = {
        "image": test_image,
        "age": "35",
        "weight": "70",
        "clinical_history": "Teste de upload de imagem"
    }
    
    # Testar API
    try:
        print("🚀 Enviando requisição para a API...")
        response = requests.post(
            "http://localhost:8000/generate_report",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Resposta recebida com sucesso!")
            print(f"🔍 Success: {data.get('success', 'N/A')}")
            print(f"📝 Report length: {len(data.get('report', ''))}")
            print(f"💬 Message: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except requests.exceptions.Timeout:
        print("⏱️ Timeout na requisição.")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

def test_image_processing():
    """Testa apenas o processamento da imagem."""
    
    try:
        from services.huggingface_service import HuggingFaceService
        
        # Criar imagem de teste
        test_image = create_test_image()
        print(f"✅ Imagem de teste criada")
        
        # Inicializar serviço (sem token para testar processamento local)
        service = HuggingFaceService("")
        
        # Testar processamento da imagem
        try:
            processed_image = service._process_image(test_image)
            print(f"✅ Imagem processada com sucesso!")
            print(f"📐 Dimensões: {processed_image.size}")
            print(f"🎨 Modo: {processed_image.mode}")
        except Exception as e:
            print(f"❌ Erro ao processar imagem: {str(e)}")
            
    except ImportError as e:
        print(f"❌ Erro de importação: {str(e)}")

if __name__ == "__main__":
    print("🔬 Teste de Upload de Imagem")
    print("=" * 50)
    
    print("\n1. Testando processamento local da imagem:")
    test_image_processing()
    
    print("\n2. Testando upload para a API:")
    test_image_upload()