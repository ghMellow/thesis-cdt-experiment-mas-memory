/* Draws every <pre class="mermaid"> with the local vendor/mermaid.min.js, in the colours of
   the current theme, and redraws when the theme changes. Load after vendor/mermaid.min.js.
   The first draw waits for document.fonts.ready: measured before IBM Plex is loaded, the
   boxes come out too narrow and the last line of each label disappears. */
(function () {
  var PAL = {
    light: { surface: "#e8ecf3", text: "#121721", line: "#5f6b7d", border: "#55627a", bg: "#ffffff" },
    dark: { surface: "#222b38", text: "#eef1f6", line: "#a3adbd", border: "#8f9bb3", bg: "#131922" }
  };
  if (typeof mermaid === "undefined") return;
  var pres = Array.prototype.slice.call(document.querySelectorAll("pre.mermaid"));
  if (!pres.length) return;
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  var root = document.documentElement;
  var items = pres.map(function (pre) {
    var mount = document.createElement("div");
    mount.className = "mermaid-diagram";
    return { pre: pre, mount: mount, src: pre.textContent || "" };
  });
  var seq = 0, gen = 0, lastKey = "";

  function render() {
    var theme = root.getAttribute("data-theme");
    var dark = theme === "dark" || (!!(mq && mq.matches) && theme !== "light");
    var pal = dark ? PAL.dark : PAL.light;
    var key = dark ? "d" : "l";
    if (key === lastKey) return;
    lastKey = key;
    var g = ++gen;
    var font = getComputedStyle(document.body).fontFamily || "sans-serif";
    var nat = { useMaxWidth: false, htmlLabels: true, curve: "basis" };
    mermaid.initialize({
      startOnLoad: false, securityLevel: "strict", theme: "base", flowchart: nat,
      themeVariables: {
        background: pal.bg, mainBkg: pal.surface, primaryColor: pal.surface,
        primaryTextColor: pal.text, lineColor: pal.line, primaryBorderColor: pal.border,
        nodeBorder: pal.border, clusterBorder: pal.border, edgeLabelBackground: pal.bg,
        clusterBkg: "rgba(127,127,127,0.07)", titleColor: pal.text, darkMode: dark,
        fontSize: "15px", fontFamily: font
      },
      themeCSS: ".node rect, .node circle, .node polygon, .node path, .cluster rect { stroke-width: 1.6px; }"
    });
    // Sequential renders: parallel ones can collide on generated ids.
    var chain = Promise.resolve();
    items.forEach(function (it) {
      chain = chain.then(function () {
        var id = "mmd-" + seq++;
        return mermaid.render(id, it.src).then(function (r) {
          if (g !== gen) return;
          it.mount.innerHTML = r.svg;
          if (!it.mount.parentNode) it.pre.parentNode.insertBefore(it.mount, it.pre);
          it.pre.style.display = "none";
        }, function (err) {
          var scratch = document.getElementById("d" + id);
          if (scratch) scratch.parentNode.removeChild(scratch);
          if (it.mount.parentNode) it.mount.parentNode.removeChild(it.mount);
          it.pre.style.display = "";
          console.error(err);
        });
      });
    });
  }
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(render);
  if (mq && mq.addEventListener) mq.addEventListener("change", render);
  if (typeof MutationObserver !== "undefined") new MutationObserver(render).observe(root, { attributes: true, attributeFilter: ["data-theme"] });
})();
