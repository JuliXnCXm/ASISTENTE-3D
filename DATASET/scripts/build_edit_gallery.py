#!/usr/bin/env python3
"""
build_edit_gallery.py
Genera una galería HTML interactiva para inspeccionar visualmente
el dataset de edición (Antes vs Después).
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = ROOT / "DATASET" / "dataset_edit_v1.json"
CREATION_PATH = ROOT / "DATASET" / "dataset_creation_v1.json"
OUTPUT_HTML = ROOT / "DATASET" / "reports" / "edit_gallery.html"

HTML_HEADER = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galería de Edición - Tesis CAD</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #333; }
        .controls { text-align: center; margin-bottom: 20px; }
        .controls select { padding: 10px; font-size: 16px; border-radius: 5px; }
        .card { background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; overflow: hidden; }
        .card-header { background: #2c3e50; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; }
        .badge { background: #e74c3c; padding: 5px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }
        .instruction { font-size: 18px; font-weight: bold; margin: 15px; text-align: center; color: #e67e22; }
        .images { display: flex; width: 100%; border-bottom: 1px solid #ddd; }
        .img-container { flex: 1; padding: 10px; text-align: center; }
        .img-container img { max-width: 100%; height: auto; border: 1px solid #eee; border-radius: 4px; }
        .img-label { font-weight: bold; margin-bottom: 10px; color: #7f8c8d; }
        .code-container { display: flex; background: #2b2b2b; color: #a9b7c6; font-family: 'Courier New', Courier, monospace; font-size: 13px; }
        .code-block { flex: 1; padding: 15px; overflow-x: auto; white-space: pre-wrap; }
        .code-block.right { border-left: 1px solid #555; }
        .highlight { color: #e6cb22; font-weight: bold; }
    </style>
    <script>
        function filterType() {
            var selectedType = document.getElementById("typeFilter").value;
            var cards = document.getElementsByClassName("card");
            for (var i = 0; i < cards.length; i++) {
                if (selectedType === "all" || cards[i].getAttribute("data-type") === selectedType) {
                    cards[i].style.display = "block";
                } else {
                    cards[i].style.display = "none";
                }
            }
        }
    </script>
</head>
<body>

    <h1>Auditoría Visual: Dataset de Edición</h1>
    
    <div class="controls">
        <label for="typeFilter">Filtrar por operación: </label>
        <select id="typeFilter" onchange="filterType()">
            <option value="all">Todas</option>
            <option value="material_change">Cambio de Material</option>
            <option value="dimension_change">Cambio de Dimensión</option>
            <option value="addition">Añadir Objeto</option>
            <option value="deletion">Eliminar Objeto</option>
            <option value="multi_deletion">Eliminación Múltiple</option>
            <option value="position_change">Desplazamiento</option>
            <option value="rotation_change">Rotación</option>
            <option value="structural_change">Cambio Estructural</option>
        </select>
    </div>
"""

HTML_FOOTER = """
</body>
</html>
"""

def diff_highlight(old_code, new_code):
    """Encuentra las diferencias y envuelve los cambios básicos en spans para resaltar."""
    # Como el AST reordena kwargs, un diff exacto línea a línea es ruidoso.
    # En vez de eso, mostramos el código crudo para que el humano juzgue.
    return old_code, new_code

def main():
    if not DATASET_PATH.exists() or not CREATION_PATH.exists():
        print("Error: No se encuentran los datasets.")
        return

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        edit_data = json.load(f)["items"]
    with open(CREATION_PATH, "r", encoding="utf-8") as f:
        creation_data = json.load(f)["items"]

    os.makedirs(OUTPUT_HTML.parent, exist_ok=True)
    
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(HTML_HEADER)
        
        # Limitar a los primeros 200 casos para que el HTML no pese 500 MB
        count = 0
        for e_id, e_item in edit_data.items():
            if count > 200:
                break
                
            base_id = e_item.get("base_scene_id")
            c_item = creation_data.get(base_id)
            if not c_item:
                continue

            before_img = "../" + c_item.get("render_path", "")
            after_img = "../" + e_item.get("after_render_path", "")
            
            # Manejo robusto de la imagen "Después"
            render_exists = os.path.exists(os.path.join(ROOT, "DATASET", e_item.get("after_render_path", "dummy")))
            if render_exists:
                after_img_tag = f'<img src="../{e_item["after_render_path"]}" alt="Después" loading="lazy">'
                after_label = "DESPUÉS (Resultado)"
            else:
                after_img_tag = f'<div style="height:250px; background:#ddd; display:flex; align-items:center; justify-content:center; color:#555;">[Render Pendiente de Blender]</div>'
                after_label = "DESPUÉS (Esperando Render)"
            
            op_type = e_item.get("edit_type", "unknown")
            instruction = e_item.get("instruction", "Sin instrucción")
            b_code, a_code = diff_highlight(e_item.get("before_python_code", ""), e_item.get("after_python_code", ""))

            card = f"""
    <div class="card" data-type="{op_type}">
        <div class="card-header">
            <span>ID: {e_id} (Base: {base_id}) | Split: {e_item.get('split', 'N/A')} | Turno: {e_item.get('turn_index', 1)}</span>
            <span class="badge">{op_type.upper()}</span>
        </div>
        <div class="instruction">🗣️ Usuario: "{instruction}"</div>
        <div class="images">
            <div class="img-container">
                <div class="img-label">ANTES (Turno Anterior)</div>
                <img src="{before_img}" alt="Antes" loading="lazy">
            </div>
            <div class="img-container">
                <div class="img-label">{after_label}</div>
                {after_img_tag}
            </div>
        </div>
        <div class="code-container">
            <div class="code-block">{b_code}</div>
            <div class="code-block right">{a_code}</div>
        </div>
    </div>
"""
            f.write(card)
            count += 1
            
        f.write(HTML_FOOTER)
        
    print(f"Galería HTML generada en: {OUTPUT_HTML}")
    print(f"Abre el archivo en tu navegador web para inspeccionar las ediciones.")

if __name__ == "__main__":
    main()
