// Aguarda o carregamento completo da página
document.addEventListener("DOMContentLoaded", function () {
  // Header scroll effect
  const header = document.querySelector(".header");
  let lastScrollTop = 0;

  window.addEventListener("scroll", function () {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > 100) {
      header.style.background = "rgba(11, 29, 38, 0.95)";
    } else {
      header.style.background = "rgba(11, 29, 38, 0.8)";
    }

    lastScrollTop = scrollTop;
  });

  // Smooth scrolling para links de navegação
  const navLinks = document.querySelectorAll(".nav a, .read-more");

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      if (targetId.startsWith("#")) {
        const targetSection = document.querySelector(targetId);
        if (targetSection) {
          const headerHeight = header.offsetHeight;
          const targetPosition = targetSection.offsetTop - headerHeight;

          window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
          });
        }
      }
    });
  });

  // Animação de entrada para elementos quando aparecem na tela
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Observar elementos de conteúdo
  const contentItems = document.querySelectorAll(
    ".content-item, .content-image"
  );
  contentItems.forEach((item) => {
    item.style.opacity = "0";
    item.style.transform = "translateY(30px)";
    item.style.transition = "opacity 0.8s ease, transform 0.8s ease";
    observer.observe(item);
  });

  // Parallax effect para backgrounds do hero
  window.addEventListener("scroll", function () {
    const scrolled = window.pageYOffset;
    const heroBgs = document.querySelectorAll(".hero-bg");

    heroBgs.forEach((bg, index) => {
      const speed = (index + 1) * 0.5;
      const yPos = -(scrolled * speed);
      bg.style.transform = `translateY(${yPos}px)`;
    });
  });

  // Navegação do slider
  const sliderIndicator = document.querySelector(".slider-indicator");
  const sliderTexts = document.querySelectorAll(".slider-text span");
  let currentSlide = 0;

  function updateSlider() {
    const indicatorHeight = 60;
    const totalHeight = 240;
    const slideHeight = totalHeight / (sliderTexts.length - 1);

    sliderIndicator.style.top = `${currentSlide * slideHeight}px`;

    // Atualizar texto ativo
    sliderTexts.forEach((text, index) => {
      if (index === currentSlide) {
        text.style.color = "#FBD784";
        text.style.fontWeight = "800";
      } else {
        text.style.color = "#ffffff";
        text.style.fontWeight = "700";
      }
    });
  }

  // Navegação por clique nos números do slider
  sliderTexts.forEach((text, index) => {
    text.addEventListener("click", function () {
      currentSlide = index;
      updateSlider();

      // Scroll para a seção correspondente
      const contentSections = document.querySelectorAll(".content-grid");
      if (contentSections[index]) {
        const headerHeight = header.offsetHeight;
        const targetPosition = contentSections[index].offsetTop - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: "smooth",
        });
      }
    });
  });

  // Atualizar slider baseado no scroll
  window.addEventListener("scroll", function () {
    const scrollTop = window.pageYOffset;
    const contentSections = document.querySelectorAll(".content-grid");

    contentSections.forEach((section, index) => {
      const sectionTop = section.offsetTop - header.offsetHeight;
      const sectionBottom = sectionTop + section.offsetHeight;

      if (scrollTop >= sectionTop && scrollTop < sectionBottom) {
        currentSlide = index;
        updateSlider();
      }
    });
  });

  // Inicializar slider
  updateSlider();

  // Hover effects para ícones sociais
  const socialIcons = document.querySelectorAll(".social-icon");

  socialIcons.forEach((icon) => {
    icon.addEventListener("mouseenter", function () {
      this.style.transform = "scale(1.2) rotate(5deg)";
    });

    icon.addEventListener("mouseleave", function () {
      this.style.transform = "scale(1) rotate(0deg)";
    });
  });

  // Animação de contador para números grandes
  function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);

    function updateCounter() {
      start += increment;
      if (start < target) {
        element.textContent = Math.floor(start);
        requestAnimationFrame(updateCounter);
      } else {
        element.textContent = target;
      }
    }

    updateCounter();
  }

  // Observar números para animação
  const numberObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const number = entry.target;
          const targetNumber = parseInt(number.textContent);
          animateCounter(number, targetNumber);
          numberObserver.unobserve(number);
        }
      });
    },
    { threshold: 0.5 }
  );

  // Observar números de conteúdo
  const contentNumbers = document.querySelectorAll(".content-number");
  contentNumbers.forEach((number) => {
    numberObserver.observe(number);
  });

  // Efeito de parallax para imagens de conteúdo
  const contentImages = document.querySelectorAll(".content-image");

  window.addEventListener("scroll", function () {
    const scrolled = window.pageYOffset;

    contentImages.forEach((image, index) => {
      const speed = 0.3 + index * 0.1;
      const yPos = -(scrolled * speed);
      image.style.transform = `translateY(${yPos}px)`;
    });
  });

  // Smooth reveal para elementos quando aparecem
  const revealElements = document.querySelectorAll(
    ".content-item h2, .content-item h3, .content-item p"
  );

  revealElements.forEach((element, index) => {
    element.style.opacity = "0";
    element.style.transform = "translateX(-30px)";
    element.style.transition = `opacity 0.6s ease ${
      index * 0.1
    }s, transform 0.6s ease ${index * 0.1}s`;

    const elementObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateX(0)";
            elementObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );

    elementObserver.observe(element);
  });

  // Efeito de hover para botões "read more"
  const readMoreLinks = document.querySelectorAll(".read-more");

  readMoreLinks.forEach((link) => {
    link.addEventListener("mouseenter", function () {
      this.style.transform = "translateX(10px)";
    });

    link.addEventListener("mouseleave", function () {
      this.style.transform = "translateX(0)";
    });
  });

  // Navegação por teclado
  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown" || e.key === "PageDown") {
      e.preventDefault();
      const currentSection = getCurrentSection();
      if (currentSection < contentSections.length - 1) {
        scrollToSection(currentSection + 1);
      }
    } else if (e.key === "ArrowUp" || e.key === "PageUp") {
      e.preventDefault();
      const currentSection = getCurrentSection();
      if (currentSection > 0) {
        scrollToSection(currentSection - 1);
      }
    }
  });

  function getCurrentSection() {
    const scrollTop = window.pageYOffset;
    const contentSections = document.querySelectorAll(".content-grid");

    for (let i = 0; i < contentSections.length; i++) {
      const sectionTop = contentSections[i].offsetTop - header.offsetHeight;
      const sectionBottom = sectionTop + contentSections[i].offsetHeight;

      if (scrollTop >= sectionTop && scrollTop < sectionBottom) {
        return i;
      }
    }
    return 0;
  }

  function scrollToSection(sectionIndex) {
    const contentSections = document.querySelectorAll(".content-grid");
    if (contentSections[sectionIndex]) {
      const headerHeight = header.offsetHeight;
      const targetPosition =
        contentSections[sectionIndex].offsetTop - headerHeight;

      window.scrollTo({
        top: targetPosition,
        behavior: "smooth",
      });
    }
  }

  // Preloader (opcional)
  window.addEventListener("load", function () {
    const preloader = document.querySelector(".preloader");
    if (preloader) {
      preloader.style.opacity = "0";
      setTimeout(() => {
        preloader.style.display = "none";
      }, 500);
    }
  });

  // Adicionar classe ativa ao link de navegação atual
  function updateActiveNavLink() {
    const scrollTop = window.pageYOffset;
    const sections = document.querySelectorAll("section[id]");

    sections.forEach((section) => {
      const sectionTop = section.offsetTop - header.offsetHeight - 100;
      const sectionBottom = sectionTop + section.offsetHeight;
      const sectionId = section.getAttribute("id");
      const navLink = document.querySelector(`.nav a[href="#${sectionId}"]`);

      if (scrollTop >= sectionTop && scrollTop < sectionBottom && navLink) {
        document
          .querySelectorAll(".nav a")
          .forEach((link) => link.classList.remove("active"));
        navLink.classList.add("active");
      }
    });
  }

  window.addEventListener("scroll", updateActiveNavLink);

  // Console log para debug
  console.log("MNTN - Site de Montanhismo carregado com sucesso!");
  console.log("Funcionalidades disponíveis:");
  console.log("- Navegação suave");
  console.log("- Efeitos de parallax");
  console.log("- Animações de entrada");
  console.log("- Navegação por slider");
  console.log("- Navegação por teclado (setas)");
});
