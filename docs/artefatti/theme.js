/* Applies the theme chosen with the menu button before first paint (load it in <head>).
   No stored choice = no attribute: prefers-color-scheme decides. */
(function () {
  var t = null;
  try { t = localStorage.getItem("mas-tema"); } catch (e) {}
  if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
})();
