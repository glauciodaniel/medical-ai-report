#!/usr/bin/env python3
"""
Teste para identificar a rota correta do endpoint Hugging Face.
"""

import asyncio
import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def test_llama_cpp_routes():
    """Testa as rotas típicas do llama.cpp server."""
    
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    base_endpoint = os.getenv("MEDGEMMA_MODEL_URL")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Rotas típicas do llama.cpp
    routes_to_test = [
        "/completion",
        "/v1/completions", 
        "/v1/chat/completions",
        "/generate",
        "/api/generate",
        "/inference"
    ]
    
    # Payloads para testar
    completion_payload = {
        "prompt": "Olá, como você está?",
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    chat_payload = {
        "messages": [
            {"role": "user", "content": "Olá, como você está?"}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    print("🧪 Testando rotas do llama.cpp server...")
    print(f"🌐 Base URL: {base_endpoint}")
    print("=" * 60)
    
    for route in routes_to_test:
        test_url = f"{base_endpoint.rstrip('/')}{route}"
        print(f"\n🔍 Testando: {route}")
        
        # Teste com completion payload
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(test_url, headers=headers, json=completion_payload)
                print(f"   Completion payload - Status: {response.status_code}")
                if response.status_code != 404:
                    print(f"   Response: {response.text[:200]}...")
                    if response.status_code == 200:
                        print(f"   ✅ ROTA FUNCIONAL ENCONTRADA: {route}")
        except Exception as e:
            print(f"   Completion payload - Erro: {str(e)}")
        
        # Teste com chat payload (apenas para rotas que parecem ser de chat)
        if "chat" in route:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(test_url, headers=headers, json=chat_payload)
                    print(f"   Chat payload - Status: {response.status_code}")
                    if response.status_code != 404:
                        print(f"   Response: {response.text[:200]}...")
                        if response.status_code == 200:
                            print(f"   ✅ ROTA FUNCIONAL ENCONTRADA: {route}")
            except Exception as e:
                print(f"   Chat payload - Erro: {str(e)}")
    
    # Teste adicional: verificar se há documentação disponível
    print(f"\n📚 Verificando documentação...")
    doc_routes = ["/docs", "/swagger", "/openapi.json", "/api/docs"]
    
    for doc_route in doc_routes:
        try:
            doc_url = f"{base_endpoint.rstrip('/')}{doc_route}"
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(doc_url, headers=headers)
                if response.status_code == 200:
                    print(f"   ✅ Documentação encontrada: {doc_route}")
                    print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_llama_cpp_routes())