/* Bryła jest nawigacją: klikalne ściany i etykiety prowadzą do sekcji.
   Przewijanie działa normalnie, więc bryła jest skrótem, a nie jedyną drogą. */

(function () {
  "use strict";

  var targets = document.querySelectorAll("[data-target]");
  if (!targets.length) return;

  function go(id) {
    var el = document.getElementById("s" + id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function paint(id, on) {
    document.querySelectorAll('[data-target="' + id + '"]').forEach(function (n) {
      n.classList.toggle("is-on", on);
    });
  }

  targets.forEach(function (node) {
    var id = node.getAttribute("data-target");

    node.addEventListener("click", function () { go(id); });
    node.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(id); }
    });

    // blok i jego etykieta podswietlaja sie razem
    node.addEventListener("mouseenter", function () { paint(id, true); });
    node.addEventListener("mouseleave", function () { paint(id, false); });
    node.addEventListener("focus", function () { paint(id, true); });
    node.addEventListener("blur", function () { paint(id, false); });
  });
})();
