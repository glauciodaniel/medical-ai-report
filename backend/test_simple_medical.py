#!/usr/bin/env python3
"""
Teste simples para verificar se o endpoint está funcionando com o novo formato.
"""

import asyncio
import httpx
import os
import base64
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

async def test_medical_analysis():
    """Testa a análise médica com uma imagem simples."""
    
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    base_url = os.getenv("MEDGEMMA_MODEL_URL")
    
    # URL correta para chat completions
    endpoint_url = f"{base_url.rstrip('/')}/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Cria uma imagem de teste simples
    test_image = Image.new('RGB', (100, 100), color='white')
    buffered = io.BytesIO()
    test_image.save(buffered, format="JPEG")
    image_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # Prompt médico simples
    prompt = """Análise esta imagem médica e forneça um relatório:
    
INSTRUÇÕES:
- Descreva os principais achados visuais
- Identifique possíveis patologias
- Forneça uma impressão diagnóstica
- Sugira próximos passos se necessário

Paciente: 40 anos"""
    
    # Payload no formato correto
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.1,
        "stream": False
    }
    
    print("🧪 Testando análise médica com novo formato...")
    print(f"🌐 Endpoint: {endpoint_url}")
    print(f"📦 Tamanho do prompt: {len(prompt)}")
    print(f"📦 Tamanho da imagem b64: {len(image_b64)}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(endpoint_url, headers=headers, json=payload)
            
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    print("✅ Análise recebida com sucesso!")
                    print(f"📄 Resposta ({len(content)} chars):")
                    print("=" * 50)
                    print(content)
                    print("=" * 50)
                else:
                    print(f"❌ Formato inesperado: {result}")
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_medical_analysis())