/* Brama i dokument.
   Bryła jest jedynym wejściem: nie ma pod nią nic do przewijania.
   Kliknięcie bloku otwiera dokument ustawiony na wybranej sekcji.
   Wewnątrz argument czyta się ciągiem, bo ma być przeczytany w trzy minuty,
   a nie zbierany po kawałku przez powroty do menu.

   Bez JavaScriptu strona zostaje zwykłą, przewijalną stroną (patrz noscript
   w index.html), więc brak skryptu nic nie psuje. */

(function () {
  "use strict";

  var body = document.body;
  var IDS = ["01", "02", "03", "04", "05"];

  body.classList.remove("no-js");
  body.classList.add("is-hub");

  function sectionOf(id) {
    return document.getElementById("s" + id);
  }

  function openDoc(id, push) {
    var el = sectionOf(id);
    if (!el) return;
    body.classList.remove("is-hub");
    body.classList.add("is-doc");
    el.scrollIntoView({ block: "start" });
    if (push !== false && location.hash !== "#s" + id) {
      history.pushState({ sec: id }, "", "#s" + id);
    }
  }

  function openHub(push) {
    body.classList.remove("is-doc");
    body.classList.add("is-hub");
    window.scrollTo(0, 0);
    if (push !== false && location.hash) {
      history.pushState({ sec: null }, "", location.pathname);
    }
  }

  /* ── bryła: bloki i etykiety ─────────────────────────────── */

  function mark(id, on) {
    document.querySelectorAll('[data-target="' + id + '"]').forEach(function (n) {
      n.classList.toggle("is-on", on);
    });
  }

  document.querySelectorAll("[data-target]").forEach(function (node) {
    var id = node.getAttribute("data-target");
    node.addEventListener("click", function (e) { e.preventDefault(); openDoc(id); });
    node.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDoc(id); }
    });
    node.addEventListener("mouseenter", function () { mark(id, true); });
    node.addEventListener("mouseleave", function () { mark(id, false); });
    node.addEventListener("focus", function () { mark(id, true); });
    node.addEventListener("blur", function () { mark(id, false); });
  });

  /* ── powrót do bryły i przejścia między sekcjami ──────────── */

  document.querySelectorAll("[data-hub]").forEach(function (node) {
    node.addEventListener("click", function (e) { e.preventDefault(); openHub(); });
  });

  document.querySelectorAll("[data-next]").forEach(function (node) {
    node.addEventListener("click", function (e) {
      e.preventDefault();
      var id = node.getAttribute("data-next");
      if (id === "hub") { openHub(); } else { openDoc(id); }
    });
  });

  /* ── historia przeglądarki: wstecz wraca do bryły ─────────── */

  window.addEventListener("popstate", function () {
    var m = /^#s(\d\d)$/.exec(location.hash);
    if (m && IDS.indexOf(m[1]) > -1) { openDoc(m[1], false); } else { openHub(false); }
  });

  /* ── wejście z linkiem bezpośrednim ──────────────────────── */

  var start = /^#s(\d\d)$/.exec(location.hash);
  if (start && IDS.indexOf(start[1]) > -1) openDoc(start[1], false);
})();
