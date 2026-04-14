/**
 * 顶栏滚动态、滚动显现、按钮涟漪（Apple 式轻交互）
 */
(function () {
  "use strict";

  const header = document.getElementById("site-header");
  let scrollTicking = false;

  function updateHeader() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
    scrollTicking = false;
  }

  function onScroll() {
    if (!scrollTicking) {
      scrollTicking = true;
      requestAnimationFrame(updateHeader);
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  updateHeader();

  /* 滚动进入视口时显现 */
  const prefersReduced =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!prefersReduced && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { root: null, rootMargin: "0px 0px -6%", threshold: 0.08 }
    );

    document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-visible"));
  }

  /* 滚动视差 */
  const heroRoot = document.getElementById("hero-parallax-root");
  const parallaxLayers = heroRoot ? heroRoot.querySelectorAll("[data-parallax-speed]") : [];

  function updateParallax() {
    if (!parallaxLayers.length) return;
    const y = window.scrollY || 0;
    parallaxLayers.forEach((el) => {
      const speed = Number(el.getAttribute("data-parallax-speed") || 0.2);
      const offset = Math.round(y * speed * -0.35);
      el.style.setProperty("--parallax-y", `${offset}px`);
    });
  }

  window.addEventListener("scroll", updateParallax, { passive: true });
  updateParallax();

  /* 3D 鼠标跟随倾斜 */
  const tiltCards = document.querySelectorAll(".js-tilt-card");
  tiltCards.forEach((card) => {
    function onMove(ev) {
      const rect = card.getBoundingClientRect();
      const px = (ev.clientX - rect.left) / rect.width;
      const py = (ev.clientY - rect.top) / rect.height;
      const rx = (0.5 - py) * 10;
      const ry = (px - 0.5) * 12;
      card.style.transform = `perspective(900px) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(
        2
      )}deg) translateY(-4px)`;
      card.style.boxShadow = "0 20px 40px rgba(0,0,0,.16)";
    }

    function onLeave() {
      card.style.transform = "";
      card.style.boxShadow = "";
    }

    card.addEventListener("mousemove", onMove, { passive: true });
    card.addEventListener("mouseleave", onLeave, { passive: true });
  });

  /* 弹射入场显现 */
  const bounceNodes = document.querySelectorAll(".reveal-bounce");
  if (!prefersReduced && "IntersectionObserver" in window && bounceNodes.length) {
    const bounceObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            bounceObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8%", threshold: 0.08 }
    );
    bounceNodes.forEach((n) => bounceObserver.observe(n));
  } else {
    bounceNodes.forEach((n) => n.classList.add("in-view"));
  }

  // 已移除按钮涟漪效果（此前在部分浏览器/缓存场景会出现按钮异常放大）
})();
