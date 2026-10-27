/* Side menu shared by the pages of docs/artefatti/.
   Chapter order lives here and in the NN_ prefix of the file names, which must agree:
   a new page is one line in CAPITOLI plus nav.css and nav.js in the page.
   Under the open page appear its sections (section[id] with an h2).
   Without JavaScript the page stays readable as it is. */
(function () {
  var CAPITOLI = [
    { gruppo: "Panoramica", voci: [
      { file: "01_sistema.html", titolo: "Il sistema e l'esempio" }
    ]},
    { gruppo: "Come gira", voci: [
      { file: "02_architettura.html", titolo: "Architettura e componenti" },
      { file: "03_prompt.html", titolo: "Come si costruisce il prompt" },
      { file: "04_pipeline.html", titolo: "Execution pipeline" },
      { file: "05_sast.html", titolo: "L'ingresso del SAST hint" }
    ]},
    { gruppo: "Come si misura", voci: [
      { file: "06_valutazione.html", titolo: "Valutazione contro le CVE" },
      { file: "07_report.html", titolo: "I report" }
    ]},
    { gruppo: "Riferimento", voci: [
      { file: "08_parametri.html", titolo: "Parametri" },
      { file: "09_divergenze.html", titolo: "Divergenze dal paper" },
      { file: "10_glossario.html", titolo: "Glossario" }
    ]},
    { gruppo: "Risultati", voci: [
      { file: "11_confronto.html", titolo: "Confronto delle corse" }
    ]}
  ];

  var qui = (location.pathname.split("/").pop() || "01_sistema.html").toLowerCase();
  if (qui === "index.html") qui = "01_sistema.html";
  var tutte = [];
  CAPITOLI.forEach(function (g) { g.voci.forEach(function (v) { tutte.push(v); }); });

  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }

  function paragrafi() {
    var out = [];
    document.querySelectorAll("section[id]").forEach(function (s) {
      var h = s.querySelector("h2");
      if (!h) return;
      out.push({ id: s.id, titolo: h.textContent.replace(/\s+/g, " ").trim() });
    });
    return out;
  }

  // Until clicked the system theme applies; the choice is kept in localStorage
  // and applied by theme.js in <head>.
  function selettoreTema(bott) {
    var root = document.documentElement;
    var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
    function corrente() {
      var t = root.getAttribute("data-theme");
      if (t === "light" || t === "dark") return t;
      return mq && mq.matches ? "dark" : "light";
    }
    function mostra() {
      var verso = corrente() === "dark" ? "chiaro" : "scuro";
      bott.textContent = verso === "chiaro" ? "☀ Tema chiaro" : "☾ Tema scuro";
      bott.setAttribute("aria-label", "Passa al tema " + verso);
    }
    bott.addEventListener("click", function () {
      var prossimo = corrente() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", prossimo);
      try { localStorage.setItem("mas-tema", prossimo); } catch (e) {}
      mostra();
    });
    if (mq && mq.addEventListener) mq.addEventListener("change", mostra);
    mostra();
  }

  function costruisci() {
    var nav = el("nav", "sidenav");
    nav.setAttribute("aria-label", "Capitoli");

    var testa = el("div", "sn-head");
    var marchio = el("a", "sn-brand", "MAS free5GC");
    marchio.href = "01_sistema.html";
    var sotto = el("span", "sn-sub", "documentazione del sistema");
    var bott = el("button", "sn-toggle", "Capitoli");
    bott.type = "button";
    bott.setAttribute("aria-expanded", "false");
    var tema = el("button", "sn-tema");
    tema.type = "button";
    testa.appendChild(marchio); testa.appendChild(sotto); testa.appendChild(tema); testa.appendChild(bott);
    selettoreTema(tema);
    nav.appendChild(testa);

    var corpo = el("div", "sn-body");
    var secs = paragrafi();
    CAPITOLI.forEach(function (g) {
      corpo.appendChild(el("div", "sn-group", g.gruppo));
      var ul = el("ul", "sn-list");
      g.voci.forEach(function (v) {
        var li = el("li");
        var a = el("a", "sn-link");
        a.href = v.file;
        a.appendChild(el("span", "sn-t", v.titolo));
        li.appendChild(a);
        if (v.file === qui) {
          a.setAttribute("aria-current", "page");
          if (secs.length) {
            var sub = el("ul", "sn-secs");
            secs.forEach(function (s) {
              var sli = el("li");
              var sa = el("a", "sn-sec", s.titolo);
              sa.href = "#" + s.id;
              sa.dataset.target = s.id;
              sli.appendChild(sa);
              sub.appendChild(sli);
            });
            li.appendChild(sub);
          }
        }
        ul.appendChild(li);
      });
      corpo.appendChild(ul);
    });
    nav.appendChild(corpo);

    bott.addEventListener("click", function () {
      var aperto = nav.classList.toggle("open");
      bott.setAttribute("aria-expanded", aperto ? "true" : "false");
    });
    corpo.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.classList.remove("open");
        bott.setAttribute("aria-expanded", "false");
      }
    });

    document.body.insertBefore(nav, document.body.firstChild);
    document.body.classList.add("has-sidenav");
    return secs;
  }

  function precSucc() {
    var i = -1;
    tutte.forEach(function (v, k) { if (v.file === qui) i = k; });
    if (i < 0) return;
    var wrap = document.querySelector(".wrap") || document.body;
    var box = el("div", "sn-pager");
    function link(v, verso) {
      var a = el("a", "sn-pg " + verso);
      a.href = v.file;
      a.appendChild(el("span", "sn-pg-k", verso === "prev" ? "← precedente" : "successivo →"));
      a.appendChild(el("span", "sn-pg-t", v.titolo));
      return a;
    }
    if (i > 0) box.appendChild(link(tutte[i - 1], "prev")); else box.appendChild(el("span"));
    if (i < tutte.length - 1) box.appendChild(link(tutte[i + 1], "next"));
    wrap.appendChild(box);
  }

  function spia(secs) {
    if (!secs.length || !("IntersectionObserver" in window)) return;
    var links = {};
    document.querySelectorAll(".sn-sec").forEach(function (a) { links[a.dataset.target] = a; });
    var visibili = {};
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visibili[en.target.id] = en.isIntersecting; });
      var primo = null;
      secs.forEach(function (s) { if (!primo && visibili[s.id]) primo = s.id; });
      if (!primo) return;
      Object.keys(links).forEach(function (k) { links[k].classList.toggle("on", k === primo); });
    }, { rootMargin: "-10% 0px -70% 0px" });
    secs.forEach(function (s) { var n = document.getElementById(s.id); if (n) obs.observe(n); });
  }

  function avvia() {
    var secs = costruisci();
    precSucc();
    spia(secs);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", avvia);
  else avvia();
})();
