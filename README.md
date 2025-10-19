# Medical AI Report

Uma aplicação completa para geração de relatórios médicos usando Inteligência Artificial, com frontend Next.js e backend FastAPI.

## Sobre o Projeto

O Medical AI Report é uma plataforma que utiliza IA para analisar imagens médicas e gerar relatórios detalhados com base nos dados do paciente. A aplicação integra modelos de IA avançados através da API do Hugging Face.

## Funcionalidades

- Upload de Imagens Médicas: Interface para envio de exames
- Análise com IA: Processamento usando modelos MedGemma-4B-IT
- Formulário de Paciente: Coleta de dados clínicos (idade, peso, histórico)
- Geração de Relatórios: Relatórios médicos detalhados e estruturados
- Interface Moderna: Design responsivo com Tailwind CSS
- Monitoramento: Application Insights e logs centralizados
- Status em Tempo Real: Verificação do status do backend

## Tecnologias Utilizadas

### Frontend (Next.js)

- Next.js 14: Framework React com App Router
- TypeScript: Tipagem estática
- Tailwind CSS: Estilização utilitária
- shadcn/ui: Componentes de UI
- React Hook Form: Gerenciamento de formulários

### Backend (FastAPI)

- FastAPI: Framework Python para APIs REST
- Uvicorn: Servidor ASGI
- Hugging Face: Integração com modelos de IA
- Pillow: Processamento de imagens
- Pydantic: Validação de dados

### Infraestrutura (Azure)

- Azure Container Apps: Hosting serverless
- Azure Container Registry: Registry de imagens Docker
- Application Insights: Monitoramento e telemetria
- Log Analytics: Centralização de logs
- Managed Identity: Autenticação segura

## Deploy e Configuração

### Backend (Azure Container Apps)

```bash
# Clone o repositório
git clone https://github.com/glauciodaniel/medical-ai-report.git
cd medical-ai-report

# Configure as variáveis de ambiente
cp backend/.env.example backend/.env
# Edite o backend/.env com seu token Hugging Face

# Deploy no Azure
azd auth login
azd up
```

### Frontend (Vercel)

1. Configure a variável de ambiente no Vercel:

   - `NEXT_PUBLIC_BACKEND_URL=https://caj7fdrvedopcpo.jollystone-49eed872.eastus2.azurecontainerapps.io`

2. Ou para desenvolvimento local:
   ```bash
   cp env.example .env.local
   # Edite .env.local com a URL do backend
   npm run dev
   ```

### URLs de Produção

- Frontend: https://medical-ai-report.vercel.app/
- Backend API: https://caj7fdrvedopcpo.jollystone-49eed872.eastus2.azurecontainerapps.io/
- API Docs: https://caj7fdrvedopcpo.jollystone-49eed872.eastus2.azurecontainerapps.io/docs

## Configuração de Desenvolvimento

### Pré-requisitos

- Node 18+
- Python 3.11+ (para o backend)
- Azure CLI / azd (opcional, para deploy)

## Estrutura do Projeto

Veja a árvore principal do repositório para localizar frontend (`app/`, `components/`) e backend (`backend/`).
