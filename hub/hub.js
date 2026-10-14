/* Shared behavior for hub pages. Any field with data-q is loaded from and saved to progress/answers/<lesson>.json.
   <body data-lesson="L5">. Radios: give every radio in a group the same name and data-q. Checkboxes save true/false. */
const Hub = (() => {
  const H = { "X-Hub": "1", "Content-Type": "application/json" };
  const lesson = document.body.dataset.lesson;
  let pending = {}, timer = null;
  const el = (s, r = document) => r.querySelector(s);
  const all = (s, r = document) => [...r.querySelectorAll(s)];

  async function api(path, method = "GET", body) {
    const r = await fetch(path, { method, headers: method === "GET" ? {} : H, body: body ? JSON.stringify(body) : undefined });
    return r.json();
  }
  function status(msg) { const s = el("#saved"); if (s) s.textContent = msg; }
  function queue(k, v) {
    pending[k] = v; status("saving...");
    clearTimeout(timer);
    timer = setTimeout(async () => {
      const send = pending; pending = {};
      try { const r = await api("/api/answers/" + lesson, "PUT", send); status("saved " + (r.updated || "").slice(11)); }
      catch (e) { status("NOT saved: is the hub running?"); Object.assign(pending, send); }
    }, 500);
  }
  function fill(d) {
    all("[data-q]").forEach(n => {
      const k = n.dataset.q, v = d[k];
      if (v === undefined) return;
      if (n.type === "radio") n.checked = (n.value === v);
      else if (n.type === "checkbox") n.checked = !!v;
      else n.value = v;
    });
  }
  function wire() {
    all("[data-q]").forEach(n => {
      const k = n.dataset.q;
      const h = () => queue(k, n.type === "checkbox" ? n.checked : n.value);
      n.addEventListener(n.type === "radio" || n.type === "checkbox" ? "change" : "input", h);
      if (n.type === "checkbox") n.addEventListener("change", sync);
    });
  }
  function sync() {
    all(".step").forEach(s => {
      const f = el("input.fin", s);
      s.classList.toggle("done", !!(f && f.checked));
    });
    all("[data-needs]").forEach(n => { const need = el('[data-q="' + n.dataset.needs + '"]'); n.hidden = !(need && need.checked); });
    all("[data-enable]").forEach(n => { const need = el('[data-q="' + n.dataset.enable + '"]'); n.disabled = !(need && need.checked); });
  }
  async function init() {
    if (lesson) {
      try { fill(await api("/api/answers/" + lesson)); } catch (e) { status("hub not reachable"); }
      wire();
    }
    sync();
  }
  async function runLab(lab, outId) {
    const o = el(outId); o.textContent = "Running tests...";
    try { const r = await api("/api/lab/" + lab, "POST", {}); o.textContent = r.output || "(no output)"; o.dataset.ok = r.ok; return r.ok; }
    catch (e) { o.textContent = "Could not reach the hub."; return false; }
  }
  function check(btn, rules) { /* rules: [{q:'id', target:123, tol:0.02, fb:'#id'}] auto-grade numeric answers */
    btn.addEventListener("click", () => {
      rules.forEach(r => {
        const v = parseFloat(String(el('[data-q="' + r.q + '"]').value).replace(/[, $]/g, ""));
        const f = el(r.fb); const okv = Math.abs(v - r.target) <= Math.abs(r.target) * (r.tol ?? 0.02);
        f.className = "fb " + (isNaN(v) ? "" : okv ? "ok" : "no");
        f.textContent = isNaN(v) ? "" : okv ? "Correct." : (r.hint || "Not quite. Recheck the arithmetic.");
      });
    });
  }
  async function nav(active) {
    const items = [["index.html", "Home"], ["cards.html", "Cards"], ["library.html", "Library"]];
    const base = location.pathname.includes("/lessons/") ? "../" : "";
    const n = el("nav.top");
    n.innerHTML = items.map(([h, t]) => `<a href="${base}${h}" class="${active === h ? "on" : ""}">${t}</a>`).join("") + '<span class="grow"></span><span id="saved"></span>';
  }
  return { init, api, runLab, check, nav, el, all, H };
})();
