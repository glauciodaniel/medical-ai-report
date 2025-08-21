#!/usr/bin/env python3
"""
Script simples para testar se a configuração está sendo carregada
"""

try:
    from config import (
        HUGGINGFACE_API_TOKEN, 
        MEDGEMMA_MODEL_URL, 
        API_HOST, 
        API_PORT,
        CORS_ORIGINS,
        MAX_NEW_TOKENS,
        TEMPERATURE,
        TOP_P,
        validate_config
    )
    
    print("✅ Configuração importada com sucesso!")
    print(f"🔑 Token: {HUGGINGFACE_API_TOKEN[:20] if HUGGINGFACE_API_TOKEN else 'NÃO CONFIGURADO'}...")
    print(f"🌐 Modelo: {MEDGEMMA_MODEL_URL}")
    print(f"🏠 Host: {API_HOST}")
    print(f"🚪 Porta: {API_PORT}")
    print(f"🔧 CORS: {CORS_ORIGINS}")
    print(f"📝 Max Tokens: {MAX_NEW_TOKENS}")
    print(f"🌡️  Temperature: {TEMPERATURE}")
    print(f"📊 Top P: {TOP_P}")
    
    # Verificar se é a URL padrão ou customizada
    if MEDGEMMA_MODEL_URL == "https://r2y80g16msuhn4pg.us-east-1.aws.endpoints.huggingface.cloud":
        print(f"📋 Modelo: {MEDGEMMA_MODEL_URL} (padrão)")
    else:
        print(f"📋 Modelo: {MEDGEMMA_MODEL_URL} (customizado)")
    
    print("\n🧪 Testando validação...")
    is_valid = validate_config()
    print(f"✅ Validação: {'PASSOU' if is_valid else 'FALHOU'}")
    
    # Verificação adicional
    print("\n🔍 Verificação detalhada:")
    print(f"   Token definido: {'✅ SIM' if HUGGINGFACE_API_TOKEN else '❌ NÃO'}")
    print(f"   URL do modelo: {'✅ SIM' if MEDGEMMA_MODEL_URL else '❌ NÃO'}")
    print(f"   Token válido: {'✅ SIM' if HUGGINGFACE_API_TOKEN and HUGGINGFACE_API_TOKEN.startswith('hf_') else '❌ NÃO'}")
    
    # Verificar se é endpoint personalizado
    if "us-east-1.aws.endpoints.huggingface.cloud" in MEDGEMMA_MODEL_URL:
        print(f"   Endpoint: {'✅ AWS Personalizado'}")
    elif "api-inference.huggingface.co" in MEDGEMMA_MODEL_URL:
        print(f"   Endpoint: {'✅ Hugging Face Oficial'}")
    else:
        print(f"   Endpoint: {'⚠️  Customizado'}")
    
except ImportError as e:
    print(f"❌ Erro ao importar configuração: {e}")
    print("Verifique se o arquivo config.py existe e está correto")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
