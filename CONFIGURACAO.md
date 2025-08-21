# Configuração da Conexão Frontend-Backend

## Visão Geral

Este projeto consiste em um frontend Next.js que se comunica com um backend Python FastAPI para gerar relatórios médicos usando IA.

## Estrutura do Projeto

```
medical-ai-report/
├── app/                    # Frontend Next.js
├── backend/               # Backend Python FastAPI
├── components/            # Componentes React
├── lib/                   # Utilitários e configurações
└── ...
```

## Configuração do Backend

### 1. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar Token da API Hugging Face

**IMPORTANTE**: Este é o passo mais importante para usar o modelo MedGemma!

Crie um arquivo `.env` na pasta `backend/` com:

```env
HUGGINGFACE_API_TOKEN=seu-token-real-aqui
```

**Como obter o token:**

1. Acesse [Hugging Face](https://huggingface.co/)
2. Faça login ou crie uma conta
3. Vá em Settings → Access Tokens
4. Crie um novo token com permissões de leitura
5. Copie o token e cole no arquivo `.env`

**Exemplo de arquivo `.env`:**

```env
HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
MEDGEMMA_MODEL_URL=https://api-inference.huggingface.co/models/google/medgemma-2b
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
MAX_NEW_TOKENS=1000
TEMPERATURE=0.7
TOP_P=0.9
```

**Configurações opcionais:**

- `MEDGEMMA_MODEL_URL`: URL do modelo (padrão: MedGemma 2B)
- `MAX_NEW_TOKENS`: Máximo de tokens gerados (padrão: 1000)
- `TEMPERATURE`: Criatividade do modelo (padrão: 0.7)
- `TOP_P`: Controle de diversidade (padrão: 0.9)

### 3. Executar o Backend

```bash
cd backend
python main.py
```

O backend estará disponível em: `http://localhost:8000`

## Configuração do Frontend

### 1. Instalar Dependências

```bash
npm install
```

### 2. Configurar URL do Backend

Crie um arquivo `.env.local` na raiz do projeto:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 3. Executar o Frontend

```bash
npm run dev
```

O frontend estará disponível em: `http://localhost:3000`

## Verificação da Conexão

### 1. Status do Backend

O componente `BackendStatus` na interface mostra:

- 🟢 **ONLINE**: Backend conectado e funcionando
- 🔴 **OFFLINE**: Backend não está acessível
- 🟡 **VERIFICANDO**: Testando conectividade

### 2. Teste Manual

Acesse: `http://localhost:8000/health`
Resposta esperada: `{"status": "healthy", "pil_available": true/false}`

### 3. Verificar Configuração do Hugging Face

O backend agora verifica automaticamente se o token está configurado:

**Se o token estiver configurado corretamente:**

- O sistema tentará usar o modelo MedGemma
- Você verá a mensagem: "Relatório gerado com sucesso usando modelo MedGemma"

**Se o token não estiver configurado:**

- Você verá a mensagem: "Token da API Hugging Face não configurado"
- O sistema retornará um relatório demonstrativo

### 4. Diagnóstico Automático

Se o modelo não estiver funcionando, execute o script de diagnóstico:

```bash
cd backend
python diagnose.py
```

Este script verificará:

- ✅ Arquivo `.env` existe e está configurado
- ✅ Variáveis de ambiente estão carregadas
- ✅ Dependências Python estão instaladas
- ✅ Configuração pode ser importada

## Endpoints da API

### Backend Python (`localhost:8000`)

- `GET /` - Página inicial
- `GET /health` - Status de saúde
- `POST /generate_report` - Gerar relatório médico

### Frontend Next.js (`localhost:3000`)

- `/` - Interface principal
- `/api/generate_report` - **DEPRECIADO** (agora chama diretamente o backend)

## Fluxo de Dados

1. **Upload de Imagem**: Usuário faz upload de imagem médica
2. **Dados do Paciente**: Preenchimento de idade, peso e histórico
3. **Requisição ao Backend**: Frontend envia dados para `localhost:8000/generate_report`
4. **Processamento IA**: Backend processa imagem com modelo MedGemma
5. **Resposta**: Relatório médico retorna para o frontend
6. **Exibição**: Relatório é mostrado na interface

## Solução de Problemas

### Backend não conecta

- Verifique se o Python está rodando na porta 8000
- Confirme se as dependências estão instaladas
- Verifique logs de erro no terminal

### CORS Errors

- O backend já está configurado com CORS habilitado
- Se persistir, verifique se o frontend está na origem permitida

### Token do Hugging Face não funciona

- Verifique se o arquivo `.env` está na pasta `backend/`
- Confirme se o token começa com `hf_`
- Teste o token no site do Hugging Face
- Verifique se o token tem permissões de leitura

### Imagem não processa com IA

- Verifique se o token da API Hugging Face está configurado corretamente
- Confirme se a imagem está em formato suportado (JPG, PNG)
- Verifique o tamanho da imagem (máximo 10MB)
- Verifique os logs do backend para erros específicos da API

### Erro "Invalid response format from Hugging Face API"

- A API do Hugging Face pode retornar diferentes formatos
- O sistema foi atualizado para lidar com múltiplos formatos
- Se persistir, verifique se o modelo MedGemma está disponível

## Configuração de Produção

### Backend

```python
# Em main.py, altere:
allow_origins=["https://seu-dominio.com"]  # Ao invés de ["*"]
```

### Frontend

```env
NEXT_PUBLIC_BACKEND_URL=https://seu-backend.com
```

## Arquivos de Configuração

- `lib/config.ts` - Configurações da API
- `env.example` - Exemplo de variáveis de ambiente
- `backend/main.py` - Configurações do servidor FastAPI

## Dependências Principais

### Backend

- FastAPI
- Uvicorn
- Pillow (PIL)
- Requests
- Transformers (Hugging Face)

### Frontend

- Next.js 14
- React
- TypeScript
- Tailwind CSS
- Shadcn/ui
