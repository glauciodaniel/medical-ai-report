#!/usr/bin/env python3
"""
Script para testar e diagnosticar o endpoint do Hugging Face.
"""

import asyncio
import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def test_endpoint_status():
    """Testa detalhadamente o endpoint do Hugging Face."""
    
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    endpoint_url = os.getenv("MEDGEMMA_MODEL_URL")
    
    if not token:
        print("❌ HUGGINGFACE_API_TOKEN não encontrado no .env")
        return
    
    if not endpoint_url:
        print("❌ MEDGEMMA_MODEL_URL não encontrado no .env")
        return
    
    print(f"🔑 Token: {token[:10]}...")
    print(f"🌐 Endpoint: {endpoint_url}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Teste 1: GET no endpoint base
    print("\n1️⃣ Testando GET no endpoint base...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(endpoint_url, headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            if response.text:
                print(f"   Response: {response.text[:300]}...")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
    
    # Teste 2: GET no /health
    print("\n2️⃣ Testando GET /health...")
    try:
        health_url = f"{endpoint_url.rstrip('/')}/health"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(health_url, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
    
    # Teste 3: GET no /info  
    print("\n3️⃣ Testando GET /info...")
    try:
        info_url = f"{endpoint_url.rstrip('/')}/info"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(info_url, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
    
    # Teste 4: POST simples
    print("\n4️⃣ Testando POST com payload simples...")
    try:
        simple_payload = {
            "inputs": "Olá, como você está?",
            "parameters": {
                "max_new_tokens": 50,
                "temperature": 0.1
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                endpoint_url, 
                headers=headers, 
                json=simple_payload
            )
            print(f"   Status: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:300]}...")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
    
    # Teste 5: Listar endpoints disponíveis na conta HF
    print("\n5️⃣ Verificando endpoints disponíveis na conta...")
    try:
        hf_api_url = "https://api-inference.huggingface.co/models"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(hf_api_url, headers=headers)
            print(f"   Status API HF: {response.status_code}")
            
            # Tentar listar endpoints privados
            endpoints_url = "https://api.endpoints.huggingface.cloud/v2/endpoint"
            response = await client.get(endpoints_url, headers=headers)
            print(f"   Status Endpoints: {response.status_code}")
            if response.status_code == 200:
                endpoints_data = response.json()
                if endpoints_data:
                    print("   📋 Endpoints encontrados:")
                    for endpoint in endpoints_data.get("items", []):
                        print(f"      - {endpoint.get('name', 'N/A')}: {endpoint.get('url', 'N/A')}")
                        print(f"        Status: {endpoint.get('status', 'N/A')}")
                else:
                    print("   📋 Nenhum endpoint privado encontrado")
            else:
                print(f"   ❌ Erro ao listar endpoints: {response.text}")
                
    except Exception as e:
        print(f"   ❌ Erro ao verificar endpoints: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Diagnóstico concluído!")

if __name__ == "__main__":
    print("🔍 Diagnóstico de Endpoint Hugging Face")
    print("Este script vai testar várias configurações para identificar o problema.")
    asyncio.run(test_endpoint_status())