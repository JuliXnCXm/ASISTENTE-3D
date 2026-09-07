# generate_gallery.py
# Genera una galería HTML interactiva para curación visual del dataset.
# Lee el JSON (con render_path por ítem) y produce gallery.html.
# En la galería puedes marcar items malos → exportar flagged_ids.json.
#
# Uso:
#   python generate_gallery.py --dataset dataset_v2_with_renders.json
#   python generate_gallery.py --dataset dataset_v2_with_renders.json --out curate/gallery.html

import json
import os
import argparse


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, help="JSON con render_path por ítem")
    ap.add_argument("--out", default=None,
                    help="Ruta del HTML generado (por defecto: gallery.html junto al JSON)")
    return ap.parse_args()


def rel_img_path(render_path, html_path, dataset_path):
    """Convierte render_path (relativo al JSON) a relativo al HTML."""
    dataset_dir = os.path.dirname(os.path.abspath(dataset_path))
    html_dir = os.path.dirname(os.path.abspath(html_path))
    abs_render = os.path.normpath(os.path.join(dataset_dir, render_path))
    return os.path.relpath(abs_render, start=html_dir).replace("\\", "/")


def build_items_js(items, html_path, dataset_path):
    rows = []
    for pid, item in items.items():
        render_path = item.get("render_path", "")
        img = rel_img_path(render_path, html_path, dataset_path) if render_path else ""
        rows.append({
            "id": pid,
            "prompt": item.get("prompt", ""),
            "tier": item.get("tier", ""),
            "domain": item.get("domain", ""),
            "category": item.get("category", ""),
            "img": img,
        })
    return json.dumps(rows, ensure_ascii=False)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dataset Curation Gallery</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #111; color: #eee; }

  /* ── Header ── */
  #header {
    position: sticky; top: 0; z-index: 100;
    background: #1a1a1a; border-bottom: 1px solid #333;
    padding: 10px 16px; display: flex; flex-wrap: wrap;
    gap: 10px; align-items: center;
  }
  #header h1 { font-size: 1rem; color: #fff; white-space: nowrap; }
  #stats { font-size: 0.82rem; color: #aaa; white-space: nowrap; }
  #stats span { color: #f87; font-weight: bold; }
  .controls { display: flex; flex-wrap: wrap; gap: 8px; flex: 1; }
  .controls input, .controls select {
    background: #252525; border: 1px solid #444; color: #eee;
    padding: 4px 8px; border-radius: 4px; font-size: 0.82rem;
  }
  .controls input { flex: 1; min-width: 180px; }
  button {
    padding: 5px 12px; border-radius: 4px; border: none;
    font-size: 0.82rem; cursor: pointer; white-space: nowrap;
  }
  #btn-export  { background: #2a7; color: #fff; }
  #btn-clear   { background: #555; color: #eee; }
  #btn-export:hover { background: #3b8; }
  #btn-clear:hover  { background: #666; }

  /* ── Grid ── */
  #grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 10px; padding: 14px;
  }

  /* ── Card ── */
  .card {
    background: #1e1e1e; border-radius: 8px; overflow: hidden;
    border: 2px solid transparent; cursor: pointer;
    transition: border-color .15s, transform .1s;
    position: relative;
  }
  .card:hover { transform: scale(1.02); }
  .card.flagged { border-color: #f44; background: #2a1111; }
  .card.flagged .flag-badge { display: flex; }

  .flag-badge {
    display: none; position: absolute; top: 6px; right: 6px;
    background: #f44; color: #fff; font-size: 0.7rem; font-weight: bold;
    padding: 2px 6px; border-radius: 10px; align-items: center; gap: 4px;
    pointer-events: none;
  }

  .card img {
    width: 100%; aspect-ratio: 4/3; object-fit: cover;
    display: block; background: #2a2a2a;
  }
  .card .no-img {
    width: 100%; aspect-ratio: 4/3; background: #2a2a2a;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; color: #666;
  }

  .card-body { padding: 8px; }
  .card-id { font-size: 0.72rem; color: #888; margin-bottom: 4px; }
  .badges { display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 6px; }
  .badge {
    font-size: 0.65rem; padding: 1px 6px; border-radius: 8px; font-weight: 600;
  }
  .badge-bpy     { background: #1a3a6a; color: #7af; }
  .badge-dsl     { background: #1a4a2a; color: #7fa; }
  .badge-mixed   { background: #3a2a1a; color: #fb7; }
  .badge-interior{ background: #2a1a4a; color: #b7f; }
  .badge-exterior{ background: #1a3a4a; color: #7df; }
  .badge-cat     { background: #2a2a2a; color: #999; }

  .card-prompt {
    font-size: 0.72rem; color: #bbb; line-height: 1.4;
    display: -webkit-box; -webkit-line-clamp: 3;
    -webkit-box-orient: vertical; overflow: hidden;
  }

  /* ── Empty state ── */
  #empty {
    display: none; grid-column: 1/-1;
    text-align: center; color: #555; padding: 60px 0; font-size: 0.9rem;
  }
</style>
</head>
<body>

<div id="header">
  <h1>Dataset Curation</h1>
  <div id="stats">Total: <b id="st-total">0</b> &nbsp;|&nbsp; Visibles: <b id="st-visible">0</b> &nbsp;|&nbsp; Marcados: <span id="st-flagged">0</span></div>
  <div class="controls">
    <input  id="search"      type="text"   placeholder="Buscar en prompt...">
    <select id="filter-tier">
      <option value="">Todos los tiers</option>
      <option value="bpy">bpy</option>
      <option value="dsl">dsl</option>
      <option value="mixed">mixed</option>
    </select>
    <select id="filter-domain">
      <option value="">Interior + Exterior</option>
      <option value="interior">interior</option>
      <option value="exterior">exterior</option>
    </select>
    <select id="filter-show">
      <option value="all">Mostrar todos</option>
      <option value="flagged">Solo marcados</option>
      <option value="ok">Solo OK</option>
      <option value="noimg">Sin imagen</option>
    </select>
    <button id="btn-clear">Limpiar selección</button>
    <button id="btn-export">Exportar marcados</button>
  </div>
</div>

<div id="grid"><div id="empty">No hay items que coincidan con los filtros.</div></div>

<script>
const ITEMS = __ITEMS_JSON__;

// Estado
const flagged = new Set(JSON.parse(localStorage.getItem("flagged") || "[]"));

function saveFlagged() {
  localStorage.setItem("flagged", JSON.stringify([...flagged]));
}

function badge(cls, text) {
  return `<span class="badge ${cls}">${text}</span>`;
}

function tierBadge(t) {
  return badge("badge-" + t, t);
}

function renderCard(item) {
  const isFlagged = flagged.has(item.id);
  const imgHtml = item.img
    ? `<img src="${item.img}" alt="${item.id}" loading="lazy">`
    : `<div class="no-img">sin render</div>`;

  return `
  <div class="card ${isFlagged ? "flagged" : ""}" data-id="${item.id}"
       data-tier="${item.tier}" data-domain="${item.domain}"
       data-prompt="${item.prompt.toLowerCase()}">
    <div class="flag-badge">✕ MARCADO</div>
    ${imgHtml}
    <div class="card-body">
      <div class="card-id">${item.id}</div>
      <div class="badges">
        ${tierBadge(item.tier)}
        ${badge("badge-" + item.domain, item.domain)}
        ${item.category ? badge("badge-cat", item.category) : ""}
      </div>
      <div class="card-prompt">${item.prompt}</div>
    </div>
  </div>`;
}

const grid = document.getElementById("grid");
const empty = document.getElementById("empty");

function buildGrid() {
  const frag = document.createDocumentFragment();
  ITEMS.forEach(item => {
    const div = document.createElement("div");
    div.innerHTML = renderCard(item);
    frag.appendChild(div.firstElementChild);
  });
  grid.innerHTML = "";
  grid.appendChild(frag);
  grid.appendChild(empty);
  updateStats();
}

function applyFilters() {
  const search = document.getElementById("search").value.toLowerCase().trim();
  const tier   = document.getElementById("filter-tier").value;
  const domain = document.getElementById("filter-domain").value;
  const show   = document.getElementById("filter-show").value;
  let visible = 0;

  grid.querySelectorAll(".card").forEach(card => {
    const id    = card.dataset.id;
    const isFl  = flagged.has(id);
    const hasImg = card.querySelector("img") !== null;

    const matchSearch = !search || card.dataset.prompt.includes(search);
    const matchTier   = !tier   || card.dataset.tier   === tier;
    const matchDomain = !domain || card.dataset.domain === domain;
    const matchShow   =
      show === "all"     ? true :
      show === "flagged" ? isFl :
      show === "ok"      ? !isFl :
      show === "noimg"   ? !hasImg : true;

    const show_ = matchSearch && matchTier && matchDomain && matchShow;
    card.style.display = show_ ? "" : "none";
    if (show_) visible++;
  });

  empty.style.display = visible === 0 ? "block" : "none";
  document.getElementById("st-visible").textContent = visible;
}

function updateStats() {
  document.getElementById("st-total").textContent   = ITEMS.length;
  document.getElementById("st-visible").textContent = ITEMS.length;
  document.getElementById("st-flagged").textContent = flagged.size;
}

// Click en card → toggle flagged
grid.addEventListener("click", e => {
  const card = e.target.closest(".card");
  if (!card) return;
  const id = card.dataset.id;
  if (flagged.has(id)) {
    flagged.delete(id);
    card.classList.remove("flagged");
    card.querySelector(".flag-badge").style.display = "none";
  } else {
    flagged.add(id);
    card.classList.add("flagged");
    card.querySelector(".flag-badge").style.display = "flex";
  }
  saveFlagged();
  document.getElementById("st-flagged").textContent = flagged.size;
});

// Filtros
["search","filter-tier","filter-domain","filter-show"].forEach(id => {
  document.getElementById(id).addEventListener("input", applyFilters);
});

// Exportar
document.getElementById("btn-export").addEventListener("click", () => {
  if (flagged.size === 0) { alert("No hay items marcados."); return; }
  const data = JSON.stringify({ flagged_ids: [...flagged].sort() }, null, 2);
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([data], { type: "application/json" }));
  a.download = "flagged_ids.json";
  a.click();
});

// Limpiar selección
document.getElementById("btn-clear").addEventListener("click", () => {
  if (!confirm(`¿Limpiar los ${flagged.size} items marcados?`)) return;
  flagged.clear();
  saveFlagged();
  grid.querySelectorAll(".card.flagged").forEach(c => {
    c.classList.remove("flagged");
    c.querySelector(".flag-badge").style.display = "none";
  });
  document.getElementById("st-flagged").textContent = 0;
});

buildGrid();
applyFilters();
</script>
</body>
</html>
"""


def main():
    args = parse_args()

    with open(args.dataset, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", {})
    if not items:
        raise SystemExit("El JSON no contiene 'items'.")

    out_html = args.out
    if not out_html:
        base = os.path.splitext(os.path.abspath(args.dataset))[0]
        out_html = base + "_gallery.html"

    os.makedirs(os.path.dirname(out_html) or ".", exist_ok=True)

    items_js = build_items_js(items, out_html, args.dataset)
    html = HTML_TEMPLATE.replace("__ITEMS_JSON__", items_js)

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)

    no_render = sum(1 for v in items.values() if not v.get("render_path"))
    print(f"[OK] Galería generada: {out_html}")
    print(f"     Items: {len(items)}  |  Sin render_path: {no_render}")
    print(f"     Abre el HTML en el navegador para curar.")


if __name__ == "__main__":
    main()
