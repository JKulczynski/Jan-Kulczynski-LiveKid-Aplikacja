/* Sekcja 03: agent, wynik na stronie.
   Czyta data/luka.json (wynik przebiegu agenta z agent/), filtruje w przeglądarce,
   buduje CSV z tego, co widać. Zero backendu, zero requestów poza własną domeną. */

(function () {
  "use strict";

  var root = document.getElementById("agent");
  if (!root) return;

  var elKind = root.querySelector("[data-agent-kind]");
  var elState = root.querySelector("[data-agent-state]");
  var elCity = root.querySelector("[data-agent-city]");
  var elNonpub = root.querySelector("[data-agent-nonpublic]");
  var elStats = root.querySelector("[data-agent-stats]");
  var elBody = root.querySelector("[data-agent-rows]");
  var elLimit = root.querySelector("[data-agent-limit]");
  var elCount = root.querySelector("[data-agent-count]");
  var elCsv = root.querySelector("[data-agent-csv]");
  var elMeta = root.querySelector("[data-agent-meta]");
  var elStatus = root.querySelector("[data-agent-status]");

  var DATA = null, VIEW = [];
  function limit() { var v = elLimit.value; return v === "all" ? Infinity : parseInt(v, 10); }

  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function fold(s) {
    return String(s || "").toLowerCase()
      .replace(/ą/g, "a").replace(/ć/g, "c").replace(/ę/g, "e").replace(/ł/g, "l").replace(/ń/g, "n")
      .replace(/ó/g, "o").replace(/ś/g, "s").replace(/ź/g, "z").replace(/ż/g, "z");
  }

  function load() {
    if (DATA) return Promise.resolve(DATA);
    elStatus.textContent = "Wczytuję wynik agenta…";
    return fetch("data/luka.json").then(function (r) { return r.json(); }).then(function (d) {
      DATA = d;
      var names = Object.keys(d.states);
      names.forEach(function (n) {
        var o = document.createElement("option"); o.value = n; o.textContent = n; elState.appendChild(o);
      });
      elMeta.textContent = "Przebieg agenta: " + d.generated + ". RSPO: " + fmt(d.source_rspo) +
        " przedszkoli i punktów. Rejestr żłobków: " + fmt(d.source_zlobki) + " żłobków i klubów. Przedszkolowo: " + fmt(d.source_pz) +
        " profili. Bez profilu: " + fmt(d.missing) + " przedszkoli i " + fmt(d.missing_z) + " żłobków.";
      elStatus.textContent = "";
      return d;
    }).catch(function () {
      elStatus.textContent = "Nie udało się wczytać wyniku. Odśwież stronę.";
    });
  }

  function apply() {
    if (!DATA) return;
    var st = elState.value, q = fold(elCity.value.trim()), onlyNP = elNonpub.checked, kind = elKind.value;
    VIEW = DATA.rows.filter(function (r) {
      if (kind && r.kat !== kind) return false;
      if (st && r.w !== st) return false;
      if (onlyNP && r.p) return false;
      if (q && fold(r.m).indexOf(q) < 0) return false;
      return true;
    });
    renderStats(st, onlyNP, q, kind);
    renderRows();
  }

  function renderStats(st, onlyNP, q, kind) {
    var rspo = 0, miss = 0, names = st ? [st] : Object.keys(DATA.states);
    names.forEach(function (k) {
      var s = DATA.states[k];
      if (kind !== "zlobek") { rspo += onlyNP ? s.nonpublic : s.rspo; miss += onlyNP ? s.missing_nonpublic : s.missing; }
      if (kind !== "przedszkole") { rspo += s.z_rspo; miss += onlyNP ? s.z_missing_nonpublic : s.z_missing; }
    });
    var onpz = rspo - (function () { var m = 0; names.forEach(function (k) { var s = DATA.states[k]; if (kind !== "zlobek") m += onlyNP ? s.missing_nonpublic : s.missing; if (kind !== "przedszkole") m += s.z_missing; }); return m; })();
    var what = kind === "zlobek" ? "żłobków i klubów" : kind === "przedszkole" ? "przedszkoli i punktów" : "placówek";
    var scope = st || "cała Polska";
    var note = onlyNP && kind !== "przedszkole" ? " (rejestr żłobków nie rozróżnia publicznych, więc liczba obejmuje wszystkie)" : "";
    elStats.innerHTML =
      '<div class="fig"><p class="fig__v">' + fmt(rspo) + '</p><p class="fig__l">' + esc(what) + ' w rejestrze, ' + esc(scope) + (onlyNP && kind === "przedszkole" ? ', tylko niepubliczne' : '') + esc(note) + '</p></div>' +
      '<div class="fig"><p class="fig__v">' + fmt(onpz) + '</p><p class="fig__l">z nazwą obecną na Przedszkolowo</p></div>' +
      '<div class="fig"><p class="fig__v">' + fmt(q ? VIEW.length : miss) + '</p><p class="fig__l">bez profilu na Przedszkolowo' + (onlyNP ? ', niepubliczne' : '') + (q ? ', miejscowość „' + esc(elCity.value.trim()) + '”' : '') + '</p></div>';
  }

  function renderRows() {
    var rows = VIEW.slice(0, limit());
    elBody.innerHTML = rows.map(function (r) {
      var www = r.www ? '<a href="' + esc(/^https?:/.test(r.www) ? r.www : "https://" + r.www) + '" target="_blank" rel="noopener">' + esc(r.www.replace(/^https?:\/\//, "").replace(/\/$/, "")) + '</a>' : '<span class="dim">brak</span>';
      var addr = [r.a, r.k].filter(Boolean).join(", ");
      var contact = [
        r.tel ? '<a href="tel:' + esc(r.tel.replace(/[^\d+]/g, "")) + '">' + esc(r.tel) + '</a>' : '',
        r.mail ? '<a href="mailto:' + esc(r.mail) + '">' + esc(r.mail) + '</a>' : ''
      ].filter(Boolean).join('<br>') || '<span class="dim">brak</span>';
      return '<tr><td><strong>' + esc(r.n) + '</strong>' + (addr ? '<br><span class="dim">' + esc(addr) + '</span>' : '') + '</td><td>' + esc(r.m) + '</td><td>' + esc(r.t) + (r.p ? '' : '<span class="tag">niepubl.</span>') + '</td><td class="num">' + (r.d == null ? '' : fmt(r.d)) + '</td><td class="contact-cell">' + contact + '</td><td>' + www + '</td></tr>';
    }).join("");
    if (!rows.length) elBody.innerHTML = '<tr><td colspan="6" class="dim">Nic nie pasuje do filtrów.</td></tr>';
    elCount.textContent = VIEW.length ? "Widać " + fmt(rows.length) + " z " + fmt(VIEW.length) : "";
    elCsv.disabled = !VIEW.length;
    elCsv.textContent = "Pobierz CSV (" + fmt(VIEW.length) + " wierszy, z telefonem i mailem)";
  }

  function csv() {
    var head = ["nazwa", "typ", "wojewodztwo", "miejscowosc", "adres", "kod", "publiczna", "liczba_dzieci", "www", "telefon", "email", "organ_prowadzacy", "id_rejestru"];
    var lines = [head.join(";")].concat(VIEW.map(function (r) {
      return [r.n, r.t, r.w, r.m, r.a, r.k, r.p ? "tak" : "nie", r.d == null ? "" : r.d, r.www, r.tel, r.mail, r.org, r.id]
        .map(function (v) { v = String(v == null ? "" : v).replace(/"/g, '""'); return /[;"\n]/.test(v) ? '"' + v + '"' : v; }).join(";");
    }));
    var blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "przedszkolowo-luka-" + (elKind.value || "wszystkie") + "-" + (elState.value ? fold(elState.value).replace(/\W+/g, "-") : "polska") + ".csv";
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }

  elKind.addEventListener("change", apply);
  elState.addEventListener("change", apply);
  elNonpub.addEventListener("change", apply);
  elCity.addEventListener("input", apply);
  elLimit.addEventListener("change", renderRows);
  elCsv.addEventListener("click", csv);

  /* wczytaj, gdy sekcja jest widoczna albo od razu, jeśli strona otwarta na #s03 */
  var started = false;
  function start() { if (started) return; started = true; load().then(function (d) { if (d) apply(); }); }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) start(); }).observe(root);
  } else { start(); }
  if (location.hash === "#s03") start();
  document.querySelectorAll('[data-target="03"], [data-next="03"]').forEach(function (n) { n.addEventListener("click", start); });
})();
