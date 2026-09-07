# evaluate_geometry.py
import bpy
import bmesh
import mathutils
import sys
import json
import os
import argparse
import traceback

def extract_vertices_from_scene():
    """Extrae todos los vértices de todos los meshes de la escena actual en coordenadas globales."""
    vertices = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            # Aplicamos transformaciones usando la matriz global del objeto
            matrix_world = obj.matrix_world
            for v in obj.data.vertices:
                vertices.append(matrix_world @ v.co)
    return vertices

def build_kdtree(vertices):
    """Construye un KDTree para búsquedas espaciales rápidas."""
    size = len(vertices)
    kd = mathutils.kdtree.KDTree(size)
    for i, v in enumerate(vertices):
        kd.insert(v, i)
    kd.balance()
    return kd

def calculate_chamfer_distance(verts_A, verts_B):
    """
    Calcula la Chamfer Distance (distancia métrica promedio) entre dos nubes de puntos A y B.
    CD(A, B) = (1/|A|) * sum_{a in A} min_{b in B} ||a - b||^2 + (1/|B|) * sum_{b in B} min_{a in A} ||b - a||^2
    """
    if not verts_A or not verts_B:
        return float('inf') # Error infinito si alguna escena está vacía

    kd_A = build_kdtree(verts_A)
    kd_B = build_kdtree(verts_B)

    # Distancia de A a B
    sum_dist_A = 0.0
    for a in verts_A:
        co, index, dist = kd_B.find(a)
        sum_dist_A += dist ** 2

    # Distancia de B a A
    sum_dist_B = 0.0
    for b in verts_B:
        co, index, dist = kd_A.find(b)
        sum_dist_B += dist ** 2

    cd = (sum_dist_A / len(verts_A)) + (sum_dist_B / len(verts_B))
    return cd

def run_script_in_clean_scene(script_path, arch_dir):
    """Limpia la escena y ejecuta un script de python."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    if arch_dir not in sys.path:
        sys.path.insert(0, arch_dir)
        
    code = open(script_path, "r", encoding="utf-8").read()
    
    # Inyectar librerías comunes para evitar fallas tontas de boilerplate de los LLMs
    g = {"__name__": "__main__"}
    try:
        import os, math, random, json
        import mathutils
        g["os"] = os
        g["sys"] = sys
        g["math"] = math
        g["random"] = random
        g["json"] = json
        g["mathutils"] = mathutils
        
        import blender_arch as A
        g["A"] = A
    except Exception:
        pass
        
    exec(compile(code, script_path, "exec"), g, g)
    return extract_vertices_from_scene()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt-script", required=True, help="Ruta al script Python de referencia (Ground Truth)")
    ap.add_argument("--pred-script", required=True, help="Ruta al script Python generado por el LLM (Prediction)")
    ap.add_argument("--arch-dir", required=True, help="Directorio que contiene blender_arch.py")
    ap.add_argument("--report", required=True, help="Ruta de salida del JSON de métricas")
    args, _ = ap.parse_known_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])

    report = {
        "execution_success": False,
        "execution_error": None,
        "chamfer_distance": None,
        "gt_vertices_count": 0,
        "pred_vertices_count": 0
    }

    try:
        # Obtener vértices del Ground Truth
        verts_gt = run_script_in_clean_scene(args.gt_script, args.arch_dir)
        report["gt_vertices_count"] = len(verts_gt)
        
        # Obtener vértices de la Predicción (Aislado, con manejo de errores)
        try:
            verts_pred = run_script_in_clean_scene(args.pred_script, args.arch_dir)
            report["execution_success"] = True
            report["pred_vertices_count"] = len(verts_pred)
            
            # Calcular la Chamfer Distance (La métrica estrella)
            cd = calculate_chamfer_distance(verts_gt, verts_pred)
            report["chamfer_distance"] = cd
            
        except Exception as e:
            report["execution_error"] = str(e)
            report["execution_success"] = False
            
    except Exception as fatal_e:
        report["execution_error"] = f"Fatal Error in GT evaluation: {fatal_e}"

    # Guardar Reporte
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()
