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

  /* ---------------------------- gallery: projects, filters, modal, before/after */
  var pgrid = document.querySelector(".proj-grid");
  if (pgrid) {
    var projects = {};
    try {
      JSON.parse(document.getElementById("projects-data").textContent)
        .forEach(function (p) { projects[p.id] = p; });
    } catch (e) { /* no data */ }

    var cards = Array.prototype.slice.call(pgrid.querySelectorAll(".proj-card"));
    var filterBtns = document.querySelectorAll(".filters button");

    var applyFilter = function (btn) {
      filterBtns.forEach(function (b) { b.classList.remove("is-active"); b.setAttribute("aria-pressed", "false"); });
      btn.classList.add("is-active"); btn.setAttribute("aria-pressed", "true");
      var f = btn.getAttribute("data-filter");
      cards.forEach(function (c) {
        c.classList.toggle("is-hidden", !(f === "all" || c.getAttribute("data-cat") === f));
      });
    };
    filterBtns.forEach(function (btn) { btn.addEventListener("click", function () { applyFilter(btn); }); });
    var wanted = new URLSearchParams(window.location.search).get("cat");
    if (wanted) {
      var mb = document.querySelector('.filters button[data-filter="' + wanted.replace(/[^a-z]/gi, "") + '"]');
      if (mb) applyFilter(mb);
    }

    /* helpers to build responsive markup from a data image {s,w,ar,alt} */
    var attr = function (s) { return String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;"); };
    var pickW = function (ws, t) { for (var i = 0; i < ws.length; i++) { if (ws[i] >= t) return ws[i]; } return ws[ws.length - 1]; };
    var picture = function (dir, im, sizes, target, loading) {
      var webp = im.w.map(function (w) { return dir + "/" + im.s + "-" + w + ".webp " + w + "w"; }).join(", ");
      var jpg = im.w.map(function (w) { return dir + "/" + im.s + "-" + w + ".jpg " + w + "w"; }).join(", ");
      var base = pickW(im.w, target);
      return '<picture><source type="image/webp" sizes="' + sizes + '" srcset="' + webp + '">' +
        '<img src="' + dir + "/" + im.s + "-" + base + '.jpg" sizes="' + sizes + '" srcset="' + jpg +
        '" alt="' + attr(im.alt) + '" loading="' + (loading || "lazy") + '" decoding="async"></picture>';
    };
    var fullUrl = function (dir, im) { return dir + "/" + im.s + "-" + im.w[im.w.length - 1] + ".jpg"; };

    /* ---------- lightbox (drives from a passed-in list) ---------- */
    var lb = document.querySelector(".lightbox");
    var lbImg = lb.querySelector("img"), lbCap = lb.querySelector(".lightbox__cap");
    var lbList = [], lbIndex = 0, lbFocus = null;
    var lbShow = function (i) {
      if (!lbList.length) return;
      lbIndex = (i + lbList.length) % lbList.length;
      var it = lbList[lbIndex];
      lbImg.style.opacity = "0";          // hide until the new image can paint
      lbImg.alt = it.alt || "";
      if (lbCap) lbCap.textContent = it.alt || "";
      lbImg.src = it.full;
      var reveal = function () { lbImg.style.opacity = "1"; };
      if (lbImg.decode) { lbImg.decode().then(reveal).catch(reveal); }
      else { lbImg.onload = reveal; }
    };
    var openLightbox = function (list, i) {
      lbList = list; lbFocus = document.activeElement; lbShow(i);
      lb.classList.add("is-open"); lb.setAttribute("aria-hidden", "false");
      document.body.classList.add("pmodal-open"); lb.querySelector(".lb-close").focus();
    };
    var closeLightbox = function () {
      lb.classList.remove("is-open"); lb.setAttribute("aria-hidden", "true");
      if (!pmodal.classList.contains("is-open")) document.body.classList.remove("pmodal-open");
      if (lbFocus) lbFocus.focus();
    };
    lb.querySelector(".lb-close").addEventListener("click", closeLightbox);
    lb.querySelector(".lb-next").addEventListener("click", function () { lbShow(lbIndex + 1); });
    lb.querySelector(".lb-prev").addEventListener("click", function () { lbShow(lbIndex - 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) closeLightbox(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") closeLightbox();
      else if (e.key === "ArrowRight") lbShow(lbIndex + 1);
      else if (e.key === "ArrowLeft") lbShow(lbIndex - 1);
    });

    /* ---------- project modal ---------- */
    var pmodal = document.querySelector(".pmodal");
    var pEye = pmodal.querySelector(".pmodal__eyebrow"),
        pTitle = pmodal.querySelector(".pmodal__title"),
        pDesc = pmodal.querySelector(".pmodal__desc"),
        pBA = pmodal.querySelector(".pmodal__ba"),
        pGrid = pmodal.querySelector(".pmodal__grid");
    var pFocus = null;
    var chevrons = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M9.5 7l-4 5 4 5M14.5 7l4 5-4 5"/></svg>';

    var openProject = function (id) {
      var p = projects[id]; if (!p) return;
      pFocus = document.activeElement;
      pEye.textContent = p.catLabel + " · " + p.subtype;
      pTitle.textContent = p.title;
      pDesc.textContent = p.desc || ""; pDesc.style.display = p.desc ? "" : "none";

      pBA.innerHTML = "";
      (p.ba || []).forEach(function (pair) {
        var ar = pair.after.ar || 0.667;
        var el = document.createElement("div");
        el.innerHTML =
          '<div class="ba__label">Before / After &middot; drag to compare</div>' +
          '<div class="ba" style="aspect-ratio:1 / ' + ar + '">' +
            '<div class="ba__after">' + picture(p.dir, pair.after, "(max-width:1040px) 92vw, 900px", 900, "eager") + '</div>' +
            '<div class="ba__before">' + picture(p.dir, pair.before, "(max-width:1040px) 92vw, 900px", 900, "eager") + '</div>' +
            '<div class="ba__handle">' + chevrons + '</div>' +
            '<span class="ba__tag ba__tag--before">Before</span>' +
            '<span class="ba__tag ba__tag--after">After</span>' +
            '<input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Reveal before or after">' +
          '</div>';
        pBA.appendChild(el);
        var stage = el.querySelector(".ba"), range = el.querySelector(".ba__range");
        range.addEventListener("input", function () { stage.style.setProperty("--pos", range.value + "%"); });
      });

      pGrid.innerHTML = "";
      var lightList = (p.photos || []).map(function (im) { return { full: fullUrl(p.dir, im), alt: im.alt }; });
      (p.photos || []).forEach(function (im, idx) {
        var b = document.createElement("button");
        b.type = "button"; b.setAttribute("aria-label", "Enlarge photo: " + im.alt);
        b.innerHTML = picture(p.dir, im, "(max-width:700px) 45vw, 220px", 400, "lazy");
        b.addEventListener("click", function () { openLightbox(lightList, idx); });
        pGrid.appendChild(b);
      });

      pmodal.classList.add("is-open"); pmodal.setAttribute("aria-hidden", "false");
      document.body.classList.add("pmodal-open");
      pmodal.querySelector(".pmodal__panel").scrollTop = 0;
      pmodal.querySelector(".pmodal__close").focus();
    };
    var closeProject = function () {
      pmodal.classList.remove("is-open"); pmodal.setAttribute("aria-hidden", "true");
      if (!lb.classList.contains("is-open")) document.body.classList.remove("pmodal-open");
      if (pFocus) pFocus.focus();
    };
    cards.forEach(function (c) { c.addEventListener("click", function () { openProject(c.getAttribute("data-id")); }); });
    pmodal.querySelectorAll("[data-pclose]").forEach(function (el) { el.addEventListener("click", closeProject); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && pmodal.classList.contains("is-open") && !lb.classList.contains("is-open")) closeProject();
    });

    /* deep link: gallery.html?project=<id> opens that project (from home tiles) */
    var wantProject = new URLSearchParams(window.location.search).get("project");
    if (wantProject && projects[wantProject]) {
      var pcard = pgrid.querySelector('.proj-card[data-id="' + wantProject.replace(/[^a-z0-9\-]/gi, "") + '"]');
      if (pcard) {
        pcard.scrollIntoView({ block: "center" });
        pcard.classList.add("is-flash");
        setTimeout(function () { pcard.classList.remove("is-flash"); }, 2200);
      }
      openProject(wantProject);
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
