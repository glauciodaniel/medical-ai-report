# Medical AI Report

Uma aplicação completa para geração de relatórios médicos usando Inteligência Artificial, com frontend Next.js e backend FastAPI.

## � Sobre o Projeto

O Medical AI Report é uma plataforma que utiliza IA para analisar imagens médicas e gerar relatórios detalhados com base nos dados do paciente. A aplicação integra modelos de IA avançados através da API do Hugging Face.

## ✨ Funcionalidades

- **Upload de Imagens Médicas**: Interface para envio de exames
- **Análise com IA**: Processamento usando modelos MedGemma-4B-IT
- **Formulário de Paciente**: Coleta de dados clínicos (idade, peso, histórico)
- **Geração de Relatórios**: Relatórios médicos detalhados e estruturados
- **Interface Moderna**: Design responsivo com Tailwind CSS
- **Monitoramento**: Application Insights e logs centralizados
- **Status em Tempo Real**: Verificação do status do backend

## 🛠️ Tecnologias Utilizadas

### Frontend (Next.js)

- **Next.js 14**: Framework React com App Router
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização utilitária
- **shadcn/ui**: Componentes de UI
- **React Hook Form**: Gerenciamento de formulários

### Backend (FastAPI)

- **FastAPI**: Framework Python para APIs REST
- **Uvicorn**: Servidor ASGI
- **Hugging Face**: Integração com modelos de IA
- **Pillow**: Processamento de imagens
- **Pydantic**: Validação de dados

### Infraestrutura (Azure)

- **Azure Container Apps**: Hosting serverless
- **Azure Container Registry**: Registry de imagens Docker
- **Application Insights**: Monitoramento e telemetria
- **Log Analytics**: Centralização de logs
- **Managed Identity**: Autenticação segura

## 🚀 Deploy e Configuração

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

1. **Configure a variável de ambiente no Vercel**:

   - `NEXT_PUBLIC_BACKEND_URL=https://caj7fdrvedopcpo.jollystone-49eed872.eastus2.azurecontainerapps.io`

2. **Ou para desenvolvimento local**:
   ```bash
   cp env.example .env.local
   # Edite .env.local com a URL do backend
   npm run dev
   ```

### URLs de Produção

- **Frontend**: https://medical-ai-report.vercel.app/
- **Backend API**: https://caj7fdrvedopcpo.jollystone-49eed872.eastus2.azurecontainerapps.io/
- **API Docs**: https://caj7fdrvedopcpo.jollystone-49eed872.eastus2.azurecontainerapps.io/docs

## � Configuração de Desenvolvimento

### Pré-requisitos

- **HTML5**: Estrutura semântica e acessível
- **CSS3**: Estilos modernos com Flexbox e Grid
- **JavaScript Vanilla**: Funcionalidades interativas sem dependências
- **Fontes Google**: Inter e Chronicle Display para tipografia
- **SVG**: Ícones vetoriais escaláveis

## 🎨 Paleta de Cores

- **Primária**: #0B1D26 (Azul escuro)
- **Secundária**: #FBD784 (Dourado)
- **Texto**: #FFFFFF (Branco)
- **Transparências**: Várias opacidades para efeitos visuais

## 📱 Responsividade

O site é totalmente responsivo e funciona perfeitamente em:

- Desktop (1920px+)
- Tablet (768px - 1024px)
- Mobile (320px - 768px)

## 🚀 Como Executar

1. Clone ou baixe os arquivos do projeto
2. Abra o arquivo `index.html` em qualquer navegador moderno
3. Ou use um servidor local para melhor experiência

### Servidor Local (Recomendado)

```bash
# Python 3
python -m http.server 8000

# Node.js
npx serve .

# PHP
php -S localhost:8000
```

## 📁 Estrutura do Projeto

```
mntn-site/
├── index.html          # Arquivo principal HTML
├── styles.css          # Estilos CSS
├── script.js           # Funcionalidades JavaScript
└── README.md           # Este arquivo
```

## 🎯 Seções do Site

1. **Header**: Navegação principal com logo MNTN
2. **Hero**: Seção principal com título e subtítulo
3. **Equipment**: Primeira seção de conteúdo sobre níveis de montanhismo
4. **About**: Segunda seção sobre equipamentos essenciais
5. **Blog**: Terceira seção sobre mapas e navegação

## 🎭 Animações e Efeitos

- **Fade In**: Elementos aparecem gradualmente
- **Slide Up**: Movimento de baixo para cima
- **Parallax**: Backgrounds se movem em velocidades diferentes
- **Hover Effects**: Interações ao passar o mouse
- **Smooth Scrolling**: Navegação suave entre seções

## 🔧 Personalização

### Cores

Para alterar as cores, edite as variáveis CSS no arquivo `styles.css`:

```css
:root {
  --primary-color: #0b1d26;
  --accent-color: #fbd784;
  --text-color: #ffffff;
}
```

### Conteúdo

Para alterar o conteúdo, edite o arquivo `index.html` nas seções correspondentes.

### Animações

Para ajustar as animações, modifique os valores no arquivo `script.js`.

## 🌐 Compatibilidade

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers modernos

## 📝 Licença

Este projeto foi criado para fins educacionais e de demonstração.

## 🤝 Contribuições

Sugestões e melhorias são sempre bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Otimizar o código

## 📞 Contato

Para dúvidas ou sugestões sobre este projeto, entre em contato através dos canais disponíveis.

---

**MNTN** - Prepare-se para as montanhas e além! 🏔️
