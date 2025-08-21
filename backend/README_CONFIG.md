# Configuração do Backend - Medical AI Report

## Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend/` com as seguintes configurações:

### 🔑 Configurações Obrigatórias

```env
# Token da API Hugging Face (OBRIGATÓRIO)
HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 🌐 Configurações Opcionais

```env
# URL do modelo (padrão: MedGemma 2B)
MEDGEMMA_MODEL_URL=https://api-inference.huggingface.co/models/google/medgemma-2b

# Configurações do servidor
API_HOST=0.0.0.0
API_PORT=8000

# Configurações CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Configurações do modelo
MAX_NEW_TOKENS=1000
TEMPERATURE=0.7
TOP_P=0.9
```

## Como Obter o Token do Hugging Face

1. Acesse [Hugging Face](https://huggingface.co/)
2. Faça login ou crie uma conta
3. Vá em **Settings** → **Access Tokens**
4. Clique em **New token**
5. Dê um nome ao token (ex: "Medical AI Report")
6. Selecione **Read** como permissão
7. Clique em **Generate token**
8. Copie o token (começa com `hf_`)
9. Cole no arquivo `.env`

## Modelos Disponíveis

### MedGemma 2B (Padrão)

- **URL**: `https://api-inference.huggingface.co/models/google/medgemma-2b`
- **Especialidade**: Análise de imagens médicas
- **Idioma**: Inglês (mas pode responder em português)

### Outros Modelos Médicos

- **MedGemma 7B**: `https://api-inference.huggingface.co/models/google/medgemma-7b`
- **MedGemma 27B**: `https://api-inference.huggingface.co/models/google/medgemma-27b`

## Testando a Configuração

### 1. Teste de Configuração

```bash
cd backend
python test_config.py
```

### 2. Teste da API Hugging Face

```bash
cd backend
python test_huggingface.py
```

### 3. Executar o Backend

```bash
cd backend
python main.py
```

## Solução de Problemas

### Token não funciona

- Verifique se começa com `hf_`
- Confirme se tem permissões de leitura
- Teste no site do Hugging Face

### Modelo não responde

- Verifique se a URL está correta
- Alguns modelos podem estar offline
- Use o modelo padrão MedGemma 2B

### Erro de CORS

- Verifique se `CORS_ORIGINS` inclui a origem do frontend
- Para desenvolvimento: `CORS_ORIGINS=http://localhost:3000`

## Exemplo Completo de .env

```env
# ========================================
# CONFIGURAÇÃO DA API HUGGING FACE
# ========================================
HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
MEDGEMMA_MODEL_URL=https://api-inference.huggingface.co/models/google/medgemma-2b

# ========================================
# CONFIGURAÇÃO DO SERVIDOR
# ========================================
API_HOST=0.0.0.0
API_PORT=8000

# ========================================
# CONFIGURAÇÃO CORS
# ========================================
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# ========================================
# CONFIGURAÇÃO DO MODELO
# ========================================
MAX_NEW_TOKENS=1000
TEMPERATURE=0.7
TOP_P=0.9
```
