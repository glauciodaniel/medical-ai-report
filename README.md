# 🏔️ MNTN - Website de Montanhismo

Um site moderno e responsivo inspirado no design do Figma para a marca MNTN, especializada em guias de montanhismo e aventuras ao ar livre.

## ✨ Características

- **Design Responsivo**: Adapta-se perfeitamente a todos os dispositivos
- **Animações Suaves**: Transições e efeitos visuais elegantes
- **Navegação Intuitiva**: Slider lateral e navegação por seções
- **Performance Otimizada**: Código limpo e eficiente
- **Acessibilidade**: Suporte a navegação por teclado e leitores de tela

## 🚀 Como Executar

### Opção 1: Abrir Diretamente

1. Baixe todos os arquivos para uma pasta
2. Abra o arquivo `index.html` em seu navegador

### Opção 2: Servidor Local (Recomendado)

1. Instale o [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) no VS Code
2. Clique com o botão direito no `index.html`
3. Selecione "Open with Live Server"

### Opção 3: Python

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

Depois acesse `http://localhost:8000`

## 📁 Estrutura dos Arquivos

```
mntn-website/
├── index.html          # Estrutura HTML principal
├── styles.css          # Estilos CSS completos
├── script.js           # Funcionalidades JavaScript
└── README.md           # Este arquivo
```

## 🎨 Componentes Principais

### Header

- Logo MNTN animado
- Menu de navegação responsivo
- Ícone de conta com efeitos hover

### Hero Section

- Título principal impactante
- Badge "A Hiking guide"
- Indicador de scroll interativo
- Links para redes sociais
- Navegação por slider lateral

### Seções de Conteúdo

- Layout alternado (esquerda/direita)
- Números grandes decorativos
- Imagens placeholder
- Links "read more" com animações

### Footer

- Informações da empresa
- Links úteis organizados
- Logo MNTN

## 🎯 Funcionalidades JavaScript

- **Navegação por Slider**: Clique nos números para navegar entre seções
- **Scroll Suave**: Navegação interna com animações
- **Efeitos de Hover**: Interações visuais em elementos clicáveis
- **Menu Mobile**: Navegação adaptada para dispositivos móveis
- **Barra de Progresso**: Indicador visual de progresso do scroll
- **Animações de Entrada**: Elementos aparecem conforme o scroll
- **Efeito Parallax**: Background com movimento durante o scroll

## 📱 Responsividade

O site é totalmente responsivo e funciona perfeitamente em:

- Desktop (1920px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🎨 Paleta de Cores

- **Primária**: `#0B1D26` (Azul escuro)
- **Secundária**: `#FBD784` (Dourado)
- **Texto**: `#FFFFFF` (Branco)
- **Gradientes**: Variações de azul para backgrounds

## 🔧 Personalização

### Alterar Cores

Edite as variáveis CSS no arquivo `styles.css`:

```css
:root {
  --primary-color: #0b1d26;
  --accent-color: #fbd784;
  --text-color: #ffffff;
}
```

### Adicionar Conteúdo

Para adicionar novas seções, siga o padrão:

```html
<div class="content-item">
  <div class="content-number">04</div>
  <div class="content-info">
    <h3>Seu Título</h3>
    <p>Descrição</p>
    <a href="#" class="read-more">read more</a>
  </div>
  <div class="content-image">
    <div class="image-placeholder"></div>
  </div>
</div>
```

## 🌐 Navegadores Suportados

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📝 Licença

Este projeto foi criado para fins educacionais e de demonstração. Sinta-se livre para usar e modificar conforme suas necessidades.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📞 Suporte

Se você tiver alguma dúvida ou problema, abra uma issue no repositório ou entre em contato.

---

**Desenvolvido com ❤️ para a comunidade de montanhismo** 🏔️
