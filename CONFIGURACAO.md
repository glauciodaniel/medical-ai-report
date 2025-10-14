# ⚙️ Configuração do Medical AI Report

## 🎨 Personalização de Cores

### Cores Principais
```css
/* Cores principais - Edite no arquivo styles.css */

/* Header e navegação */
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Botão principal */
.generate-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

/* Relatório - cabeçalho */
.report-header {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

/* Botões de ação */
.download-btn {
    background: #10b981;
}

.print-btn {
    background: #6b7280;
}
```

### Paleta de Cores Completa
```css
:root {
    /* Cores primárias */
    --primary-blue: #667eea;
    --primary-purple: #764ba2;
    --primary-pink: #f093fb;
    --primary-red: #f5576c;
    
    /* Cores de status */
    --success-green: #10b981;
    --warning-yellow: #f59e0b;
    --error-red: #ef4444;
    --info-blue: #3b82f6;
    
    /* Cores neutras */
    --text-dark: #1e293b;
    --text-medium: #64748b;
    --text-light: #94a3b8;
    --background-light: #f8fafc;
    --border-color: #e5e7eb;
}
```

## 🔤 Personalização de Fontes

### Google Fonts
```html
<!-- No arquivo index.html, linha 8 -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Alterar Fonte Principal
```css
/* No arquivo styles.css */
body {
    font-family: 'Sua Fonte', 'Inter', sans-serif;
}
```

### Tamanhos de Fonte
```css
/* Títulos */
.hero h1 { font-size: 3rem; }
.form-header h2 { font-size: 2rem; }
.report-header h2 { font-size: 1.5rem; }

/* Texto do corpo */
body { font-size: 1rem; }
.hero p { font-size: 1.2rem; }
.form-header p { font-size: 1.1rem; }
```

## 📱 Configuração de Responsividade

### Breakpoints
```css
/* Tablet */
@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
    }
}

/* Mobile */
@media (max-width: 480px) {
    .hero h1 {
        font-size: 1.5rem;
    }
}
```

### Container Width
```css
.container {
    max-width: 1200px; /* Alterar para diferentes tamanhos */
    margin: 0 auto;
    padding: 0 20px;
}
```

## 🎯 Personalização de Funcionalidades

### Limite de Upload
```javascript
// No arquivo script.js, linha 95
if (file.size > 10 * 1024 * 1024) { // 10MB limit
    showNotification('Arquivo muito grande. Tamanho máximo: 10MB.', 'error');
    return false;
}
```

### Tempo de Simulação
```javascript
// No arquivo script.js, linha 320
async function simulateReportGeneration() {
    return new Promise((resolve) => {
        setTimeout(resolve, 3000); // 3 segundos - alterar conforme necessário
    });
}
```

### Validação de Campos
```javascript
// No arquivo script.js, linha 300
const requiredFields = [
    'patientName', 
    'patientAge', 
    'patientGender', 
    'patientWeight', 
    'patientHeight', 
    'patientSymptoms'
];
```

## 🖼️ Personalização de Imagens e Ícones

### Ícones Font Awesome
```html
<!-- No arquivo index.html, linha 9 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
```

### Alterar Ícones
```html
<!-- Logo -->
<i class="fas fa-brain"></i> <!-- Alterar para outro ícone -->

<!-- Upload -->
<i class="fas fa-cloud-upload-alt"></i>

<!-- Botão gerar -->
<i class="fas fa-magic"></i>

<!-- Botões de ação -->
<i class="fas fa-download"></i>
<i class="fas fa-print"></i>
```

### Adicionar Imagens de Fundo
```css
.hero {
    background-image: url('sua-imagem.jpg');
    background-size: cover;
    background-position: center;
}
```

## 📝 Personalização de Textos

### Textos Principais
```html
<!-- Título principal -->
<h1>Sistema de Diagnóstico Inteligente</h1>

<!-- Subtítulo -->
<p>Utilize inteligência artificial para gerar relatórios médicos precisos e detalhados</p>

<!-- Título do formulário -->
<h2>Informações do Paciente</h2>

<!-- Botão principal -->
<button type="submit" class="generate-btn">
    <i class="fas fa-magic"></i>
    Gerar Relatório
</button>
```

### Mensagens de Validação
```javascript
// No arquivo script.js
showNotification('Por favor, selecione apenas arquivos de imagem.', 'error');
showNotification('Arquivo muito grande. Tamanho máximo: 10MB.', 'error');
showNotification('Relatório gerado com sucesso!', 'success');
```

## 🔧 Configurações Avançadas

### Animações CSS
```css
/* Velocidade das transições */
* {
    transition: all 0.3s ease; /* Alterar 0.3s para velocidade desejada */
}

/* Animações personalizadas */
@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
```

### Notificações
```javascript
// Duração das notificações
setTimeout(() => {
    if (notification.parentElement) {
        notification.remove();
    }
}, 5000); // 5 segundos - alterar conforme necessário
```

### Z-Index
```css
/* Camadas de elementos */
.header { z-index: 1000; }
.loading-modal { z-index: 2000; }
.notification { z-index: 3000; }
```

## 🌐 Configurações de SEO

### Meta Tags
```html
<!-- No arquivo index.html -->
<meta name="description" content="Sistema de diagnóstico médico inteligente usando IA">
<meta name="keywords" content="medicina, IA, diagnóstico, relatórios médicos">
<meta name="author" content="Seu Nome">
<meta name="robots" content="index, follow">
```

### Open Graph
```html
<meta property="og:title" content="Medical AI Report">
<meta property="og:description" content="Sistema de diagnóstico inteligente">
<meta property="og:type" content="website">
<meta property="og:url" content="https://seusite.com">
```

## 📊 Configurações de Performance

### Otimizações CSS
```css
/* Usar transform em vez de propriedades que causam reflow */
.element:hover {
    transform: translateY(-2px); /* Melhor performance */
}

/* Evitar animações em propriedades que causam reflow */
.element:hover {
    /* ❌ Evitar */
    margin-top: -2px;
    
    /* ✅ Usar */
    transform: translateY(-2px);
}
```

### Lazy Loading
```html
<!-- Para imagens futuras -->
<img src="imagem.jpg" loading="lazy" alt="Descrição">
```

## 🚀 Configurações de Deploy

### Variáveis de Ambiente
```javascript
// Para futuras integrações com APIs
const API_BASE_URL = 'https://sua-api.com';
const API_KEY = 'sua-chave-api';
```

### Configurações de Build
```json
// package.json para futuras funcionalidades
{
  "scripts": {
    "build": "webpack --mode production",
    "dev": "webpack serve --mode development"
  }
}
```

## 🔒 Configurações de Segurança

### Headers de Segurança
```html
<!-- Para servidores que suportam -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'">
<meta http-equiv="X-Frame-Options" content="DENY">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
```

### Validação de Entrada
```javascript
// Sempre validar dados do usuário
function sanitizeInput(input) {
    return input.replace(/[<>]/g, '');
}
```

---

**💡 Use estas configurações para personalizar o site conforme suas necessidades específicas!**
