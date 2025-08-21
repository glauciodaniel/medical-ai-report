// Aguarda o carregamento completo da página
document.addEventListener("DOMContentLoaded", function () {
  // Elementos do DOM
  const header = document.querySelector(".header");
  const sliderNumbers = document.querySelectorAll(".slider-number");
  const sliderIndicator = document.querySelector(".slider-indicator");
  const scrollIndicator = document.querySelector(".scroll-indicator");
  const navLinks = document.querySelectorAll(".nav-link");

  // Header scroll effect
  window.addEventListener("scroll", function () {
    if (window.scrollY > 100) {
      header.style.background = "rgba(11, 29, 38, 0.95)";
      header.style.boxShadow = "0 4px 20px rgba(0, 0, 0, 0.3)";
    } else {
      header.style.background = "rgba(11, 29, 38, 0.8)";
      header.style.boxShadow = "none";
    }
  });

  // Slider navigation functionality
  sliderNumbers.forEach((number, index) => {
    number.addEventListener("click", function () {
      // Remove active class from all numbers
      sliderNumbers.forEach((n) => n.classList.remove("active"));

      // Add active class to clicked number
      this.classList.add("active");

      // Move slider indicator
      const indicatorPosition = index * 60;
      sliderIndicator.style.top = indicatorPosition + "px";

      // Scroll to corresponding content section
      const contentSections = document.querySelectorAll(".content-item");
      if (contentSections[index]) {
        contentSections[index].scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }
    });
  });

  // Scroll indicator functionality
  scrollIndicator.addEventListener("click", function () {
    const contentSection = document.querySelector(".content-section");
    contentSection.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });

  // Navigation link active state
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      // Remove active class from all links
      navLinks.forEach((l) => l.classList.remove("active"));

      // Add active class to clicked link
      this.classList.add("active");

      // Smooth scroll to section
      const targetId = this.getAttribute("href").substring(1);
      const targetSection = document.getElementById(targetId);

      if (targetSection) {
        e.preventDefault();
        targetSection.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Intersection Observer for content animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const contentObserver = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Observe content items for animation
  const contentItems = document.querySelectorAll(".content-item");
  contentItems.forEach((item) => {
    item.style.opacity = "0";
    item.style.transform = "translateY(50px)";
    item.style.transition = "opacity 0.8s ease, transform 0.8s ease";
    contentObserver.observe(item);
  });

  // Parallax effect for hero background
  window.addEventListener("scroll", function () {
    const scrolled = window.pageYOffset;
    const heroBg = document.querySelector(".hero-bg-image");

    if (heroBg) {
      const rate = scrolled * -0.5;
      heroBg.style.transform = `translateY(${rate}px)`;
    }
  });

  // Smooth reveal animation for content numbers
  const numberObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const number = entry.target;
          number.style.opacity = "0.3";
          number.style.transform = "scale(1)";
        }
      });
    },
    { threshold: 0.5 }
  );

  const contentNumbers = document.querySelectorAll(".content-number");
  contentNumbers.forEach((number) => {
    number.style.opacity = "0";
    number.style.transform = "scale(0.8)";
    number.style.transition = "opacity 1s ease, transform 1s ease";
    numberObserver.observe(number);
  });

  // Hover effects for social icons
  const socialIcons = document.querySelectorAll(".social-icon");
  socialIcons.forEach((icon) => {
    icon.addEventListener("mouseenter", function () {
      this.style.transform = "scale(1.1) rotate(5deg)";
    });

    icon.addEventListener("mouseleave", function () {
      this.style.transform = "scale(1) rotate(0deg)";
    });
  });

  // Account icon hover effect
  const accountIcon = document.querySelector(".account-icon");
  if (accountIcon) {
    accountIcon.addEventListener("mouseenter", function () {
      this.style.transform = "scale(1.1)";
    });

    accountIcon.addEventListener("mouseleave", function () {
      this.style.transform = "scale(1)";
    });
  }

  // Read more links hover effect
  const readMoreLinks = document.querySelectorAll(".read-more");
  readMoreLinks.forEach((link) => {
    link.addEventListener("mouseenter", function () {
      this.style.transform = "translateX(10px)";
    });

    link.addEventListener("mouseleave", function () {
      this.style.transform = "translateX(0)";
    });
  });

  // Smooth scroll for all internal links
  const internalLinks = document.querySelectorAll('a[href^="#"]');
  internalLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href");

      if (href !== "#") {
        e.preventDefault();
        const targetElement = document.querySelector(href);

        if (targetElement) {
          const headerHeight = header.offsetHeight;
          const targetPosition = targetElement.offsetTop - headerHeight - 20;

          window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
          });
        }
      }
    });
  });

  // Add loading animation
  window.addEventListener("load", function () {
    document.body.classList.add("loaded");
  });

  // Mobile menu toggle (for smaller screens)
  const createMobileMenu = () => {
    if (window.innerWidth <= 768) {
      const nav = document.querySelector(".nav");
      const account = document.querySelector(".account");

      if (nav && !document.querySelector(".mobile-menu-toggle")) {
        const toggle = document.createElement("button");
        toggle.className = "mobile-menu-toggle";
        toggle.innerHTML = `
                    <span></span>
                    <span></span>
                    <span></span>
                `;

        toggle.addEventListener("click", function () {
          nav.classList.toggle("active");
          this.classList.toggle("active");
        });

        header.querySelector(".container").insertBefore(toggle, nav);

        // Add mobile menu styles
        const style = document.createElement("style");
        style.textContent = `
                    .mobile-menu-toggle {
                        display: none;
                        flex-direction: column;
                        background: none;
                        border: none;
                        cursor: pointer;
                        padding: 5px;
                    }
                    
                    .mobile-menu-toggle span {
                        width: 25px;
                        height: 3px;
                        background: #FFFFFF;
                        margin: 3px 0;
                        transition: 0.3s;
                    }
                    
                    .mobile-menu-toggle.active span:nth-child(1) {
                        transform: rotate(-45deg) translate(-5px, 6px);
                    }
                    
                    .mobile-menu-toggle.active span:nth-child(2) {
                        opacity: 0;
                    }
                    
                    .mobile-menu-toggle.active span:nth-child(3) {
                        transform: rotate(45deg) translate(-5px, -6px);
                    }
                    
                    @media (max-width: 768px) {
                        .mobile-menu-toggle {
                            display: flex;
                        }
                        
                        .nav {
                            display: none;
                            width: 100%;
                            text-align: center;
                        }
                        
                        .nav.active {
                            display: flex;
                            flex-direction: column;
                            gap: 15px;
                        }
                        
                        .header .container {
                            flex-wrap: wrap;
                        }
                    }
                `;
        document.head.appendChild(style);
      }
    }
  };

  // Initialize mobile menu
  createMobileMenu();
  window.addEventListener("resize", createMobileMenu);

  // Add scroll progress indicator
  const createScrollProgress = () => {
    if (!document.querySelector(".scroll-progress")) {
      const progressBar = document.createElement("div");
      progressBar.className = "scroll-progress";
      progressBar.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 0%;
                height: 3px;
                background: linear-gradient(90deg, #FBD784, #FFFFFF);
                z-index: 1001;
                transition: width 0.1s ease;
            `;

      document.body.appendChild(progressBar);

      window.addEventListener("scroll", function () {
        const scrolled =
          (window.pageYOffset /
            (document.documentElement.scrollHeight - window.innerHeight)) *
          100;
        progressBar.style.width = scrolled + "%";
      });
    }
  };

  createScrollProgress();

  // Add keyboard navigation support
  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown" && window.pageYOffset < 100) {
      e.preventDefault();
      scrollIndicator.click();
    }

    if (e.key === "Escape") {
      const mobileMenu = document.querySelector(".nav.active");
      if (mobileMenu) {
        mobileMenu.classList.remove("active");
        document
          .querySelector(".mobile-menu-toggle")
          ?.classList.remove("active");
      }
    }
  });

  // Performance optimization: Throttle scroll events
  let ticking = false;

  function updateOnScroll() {
    // Update scroll-based animations here
    ticking = false;
  }

  function requestTick() {
    if (!ticking) {
      requestAnimationFrame(updateOnScroll);
      ticking = true;
    }
  }

  window.addEventListener("scroll", requestTick);

  console.log("MNTN Website loaded successfully! 🏔️");
});

