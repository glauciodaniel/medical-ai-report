#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas de configuração
"""

import os
from pathlib import Path

def check_env_file():
    """Verifica se o arquivo .env existe e está configurado"""
    print("🔍 Verificando arquivo .env...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Arquivo .env não encontrado!")
        print("   Crie um arquivo .env na pasta backend/ com:")
        print("   HUGGINGFACE_API_TOKEN=seu-token-aqui")
        return False
    
    print("✅ Arquivo .env encontrado")
    
    # Ler e verificar conteúdo
    with open(env_path, 'r') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    token_line = None
    
    for line in lines:
        if line.startswith('HUGGINGFACE_API_TOKEN='):
            token_line = line
            break
    
    if not token_line:
        print("❌ HUGGINGFACE_API_TOKEN não encontrado no arquivo .env")
        return False
    
    token = token_line.split('=', 1)[1].strip()
    
    if not token or token == 'seu-token-aqui':
        print("❌ HUGGINGFACE_API_TOKEN não configurado corretamente")
        print(f"   Valor atual: '{token}'")
        return False
    
    if not token.startswith('hf_'):
        print("❌ Token não começa com 'hf_'")
        print(f"   Token: {token[:20]}...")
        return False
    
    print(f"✅ Token configurado: {token[:20]}...")
    return True

def check_environment_variables():
    """Verifica variáveis de ambiente"""
    print("\n🔍 Verificando variáveis de ambiente...")
    
    # Verificar se python-dotenv está instalado
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv instalado")
    except ImportError:
        print("❌ python-dotenv não instalado")
        print("   Execute: pip install python-dotenv")
        return False
    
    # Carregar variáveis
    load_dotenv()
    
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    model_url = os.getenv("MEDGEMMA_MODEL_URL")
    
    print(f"   HUGGINGFACE_API_TOKEN: {'✅ Configurado' if token else '❌ Não configurado'}")
    print(f"   MEDGEMMA_MODEL_URL: {'✅ Configurado' if model_url else '❌ Não configurado'}")
    
    if token:
        print(f"   Token: {token[:20]}...")
        if not token.startswith('hf_'):
            print("   ⚠️  Token não começa com 'hf_'")
    
    return bool(token)

def check_dependencies():
    """Verifica dependências Python"""
    print("\n🔍 Verificando dependências...")
    
    dependencies = {
        'requests': 'HTTP requests',
        'PIL': 'Processamento de imagem',
        'fastapi': 'Framework web',
        'uvicorn': 'Servidor ASGI'
    }
    
    all_ok = True
    
    for module, description in dependencies.items():
        try:
            if module == 'PIL':
                import PIL
                print(f"✅ {description}: OK")
            else:
                __import__(module)
                print(f"✅ {description}: OK")
        except ImportError:
            print(f"❌ {description}: Não instalado")
            all_ok = False
    
    return all_ok

def check_config_import():
    """Verifica se o arquivo config.py pode ser importado"""
    print("\n🔍 Verificando importação da configuração...")
    
    try:
        from config import (
            HUGGINGFACE_API_TOKEN,
            MEDGEMMA_MODEL_URL,
            validate_config
        )
        print("✅ Configuração importada com sucesso")
        
        print(f"   Token: {HUGGINGFACE_API_TOKEN[:20] if HUGGINGFACE_API_TOKEN else 'NÃO CONFIGURADO'}...")
        print(f"   Modelo: {MEDGEMMA_MODEL_URL}")
        
        # Testar validação
        is_valid = validate_config()
        print(f"   Validação: {'✅ PASSOU' if is_valid else '❌ FALHOU'}")
        
        return is_valid
        
    except ImportError as e:
        print(f"❌ Erro ao importar configuração: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Executa todos os diagnósticos"""
    print("🏥 DIAGNÓSTICO DO BACKEND - Medical AI Report")
    print("=" * 60)
    
    results = []
    
    # Verificar arquivo .env
    results.append(check_env_file())
    
    # Verificar variáveis de ambiente
    results.append(check_environment_variables())
    
    # Verificar dependências
    results.append(check_dependencies())
    
    # Verificar importação da configuração
    results.append(check_config_import())
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DO DIAGNÓSTICO:")
    
    if all(results):
        print("🎉 TUDO FUNCIONANDO! O backend deve conseguir usar o modelo MedGemma")
        print("\n🚀 Para testar:")
        print("   1. python test_huggingface.py")
        print("   2. python main.py")
    else:
        print("⚠️  PROBLEMAS IDENTIFICADOS:")
        if not results[0]:
            print("   - Configure o arquivo .env com HUGGINGFACE_API_TOKEN")
        if not results[1]:
            print("   - Verifique se as variáveis de ambiente estão carregadas")
        if not results[2]:
            print("   - Instale as dependências: pip install -r requirements.txt")
        if not results[3]:
            print("   - Verifique se o arquivo config.py está correto")
        
        print("\n🔧 SOLUÇÃO:")
        print("   1. Crie um arquivo .env na pasta backend/")
        print("   2. Adicione: HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("   3. Execute: pip install -r requirements.txt")
        print("   4. Teste: python diagnose.py")

if __name__ == "__main__":
    main()
