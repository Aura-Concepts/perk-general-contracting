/* Perk General Contracting — lightweight site interactions
   No dependencies. Nav, scroll-aware header, reveal-on-scroll,
   gallery filtering + accessible lightbox, and contact form UX. */
(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------- mobile nav toggle */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ----------------------------------------------- scroll-aware header */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 40);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* --------------------------------------------- reveal on scroll (IO) */
  var revealEls = document.querySelectorAll(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* set footer year */
  var yr = document.getElementById("year");
  if (yr) yr.textContent = new Date().getFullYear();

  /* --------------------------------------------- gallery filter + lightbox */
  var grid = document.querySelector(".gallery-grid");
  if (grid) {
    var items = Array.prototype.slice.call(grid.querySelectorAll(".g-item"));
    var filterBtns = document.querySelectorAll(".filters button");

    var applyFilter = function (btn) {
      filterBtns.forEach(function (b) { b.classList.remove("is-active"); b.setAttribute("aria-pressed", "false"); });
      btn.classList.add("is-active");
      btn.setAttribute("aria-pressed", "true");
      var f = btn.getAttribute("data-filter");
      items.forEach(function (it) {
        var show = f === "all" || it.getAttribute("data-cat") === f;
        it.classList.toggle("is-hidden", !show);
      });
    };
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () { applyFilter(btn); });
    });
    /* deep-link support: gallery.html?cat=commercial */
    var params = new URLSearchParams(window.location.search);
    var wanted = params.get("cat");
    if (wanted) {
      var match = document.querySelector('.filters button[data-filter="' + wanted.replace(/[^a-z]/gi, "") + '"]');
      if (match) applyFilter(match);
    }

    /* Lightbox */
    var lb = document.querySelector(".lightbox");
    var lbImg = lb ? lb.querySelector("img") : null;
    var lbCap = lb ? lb.querySelector(".lightbox__cap") : null;
    var visible = function () { return items.filter(function (i) { return !i.classList.contains("is-hidden"); }); };
    var current = 0;
    var lastFocus = null;

    var show = function (idx) {
      var list = visible();
      if (!list.length) return;
      current = (idx + list.length) % list.length;
      var el = list[current];
      lbImg.src = el.getAttribute("data-full");
      lbImg.alt = el.getAttribute("data-alt") || "";
      if (lbCap) lbCap.textContent = el.getAttribute("data-alt") || "";
    };
    var open = function (el) {
      if (!lb) return;
      lastFocus = document.activeElement;
      show(visible().indexOf(el));
      lb.classList.add("is-open");
      lb.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      lb.querySelector(".lb-close").focus();
    };
    var close = function () {
      lb.classList.remove("is-open");
      lb.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    };

    items.forEach(function (it) {
      it.addEventListener("click", function (e) { e.preventDefault(); open(it); });
    });

    if (lb) {
      lb.querySelector(".lb-close").addEventListener("click", close);
      lb.querySelector(".lb-next").addEventListener("click", function () { show(current + 1); });
      lb.querySelector(".lb-prev").addEventListener("click", function () { show(current - 1); });
      lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
      document.addEventListener("keydown", function (e) {
        if (!lb.classList.contains("is-open")) return;
        if (e.key === "Escape") close();
        else if (e.key === "ArrowRight") show(current + 1);
        else if (e.key === "ArrowLeft") show(current - 1);
      });
    }
  }

  /* --------------------------------------------------- contact form UX */
  var form = document.querySelector(".form form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var success = document.querySelector(".form__success");
      var fields = form.querySelector(".form__fields");
      if (success && fields) {
        fields.style.display = "none";
        success.classList.add("is-visible");
        success.setAttribute("role", "status");
      }
      /* NOTE: wire up to a real handler (Formspree / Netlify / email service)
         by setting the form action + method. This is a front-end demo submit. */
    });
  }

  /* --------------------------------------------- traditional ampersand
     Archivo's "&" reads like an "e". Wrap ampersands in headings in a
     .amp span so they render in Inter's traditional looped form. */
  (function () {
    var wrap = function (el) {
      Array.prototype.slice.call(el.childNodes).forEach(function (node) {
        if (node.nodeType === 3) {
          if (node.nodeValue.indexOf("&") === -1) return;
          var parts = node.nodeValue.split("&");
          var frag = document.createDocumentFragment();
          parts.forEach(function (part, i) {
            if (i > 0) {
              var s = document.createElement("span");
              s.className = "amp";
              s.textContent = "&";
              frag.appendChild(s);
            }
            frag.appendChild(document.createTextNode(part));
          });
          node.parentNode.replaceChild(frag, node);
        } else if (node.nodeType === 1 && !node.classList.contains("amp")) {
          wrap(node);
        }
      });
    };
    document.querySelectorAll("h1, h2, h3, h4").forEach(wrap);
  })();
})();
