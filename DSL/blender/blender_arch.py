# blender_arch.py
# ---------------------------------------------------------
# Librería DSL atómica y paramétrica para arquitectura en Blender
# Dominio: AEC (Architecture, Engineering and Construction)
# Requiere: ejecutar dentro de Blender (bpy, bmesh)
# Unidades: metros. Ejes: X=ancho, Y=fondo/profundidad, Z=alto
# Cada función pública crea un activo autocontenido con un root
# (Empty) y metadatos serializados en propiedades custom.
# ---------------------------------------------------------

import bpy
import bmesh
import json
import os
from math import radians, pi, cos, sin
from mathutils import Vector, Matrix, Euler

__all__ = [
    # -- Materiales --
    "asignar_material",
    # -- Elementos estructurales --
    "crear_muro",
    "crear_columna",
    "crear_losa_rectangular",
    "crear_piso",
    "crear_techo_plano",
    "crear_tejado_dos_aguas",
    # -- Huecos y aberturas --
    "crear_ventana",
    "crear_puerta",
    "abrir_vanos_batch_rectangulares",
    "abrir_vanos_grid_local",
    # -- Escaleras y circulación --
    "crear_escalera_recta",
    "crear_baranda_lineal",
    # -- Mobiliario interior --
    "crear_mesa",
    "crear_silla",
    "crear_sofa",
    "crear_cama",
    "crear_estanteria",
    "crear_armario",
    # -- Elementos exteriores --
    "crear_terreno_plano",
    "crear_arbol_simple",
    # -- Composites de alto nivel --
    "crear_habitacion",
    "crear_casa_n_pisos",
    "crear_edificio_n_pisos",
    # -- Geometría genérica --
    "extruir_perfil",
    "extruir_con_huecos",
    "crear_tuberia",
    # -- Iluminación y cámara --
    "agregar_luz",
    "crear_camara",
    # -- Utilidades de escena --
    "anclar_a",
    "limpiar_escena",
    "exportar_escena",
    # -- Validación --
    "validar_malla",
]

# ---------------------------------------------------------
#  HELPERS INTERNOS  (prefijo _)
# ---------------------------------------------------------

def _first_mesh_child(root_or_obj):
    """Devuelve el primer hijo MESH si pasas un root (Empty).
    Si pasas un MESH directamente, lo retorna tal cual."""
    if isinstance(root_or_obj, bpy.types.Object):
        if root_or_obj.type == 'MESH':
            return root_or_obj
        if root_or_obj.type == 'EMPTY':
            for ch in root_or_obj.children:
                if ch.type == 'MESH':
                    return ch
    raise ValueError(
        "No se encontró objeto MESH válido. "
        "Pasa el root del activo o el MESH directamente."
    )


def _ensure_collection(name):
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def _new_mesh_object(name, verts, faces):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def _box(name, sx, sy, sz):
    """Caja con origen en esquina mínima (0,0,0) → (sx, sy, sz)."""
    verts = [
        (0,  0,  0),  (sx, 0,  0),  (sx, sy, 0),  (0,  sy, 0),
        (0,  0,  sz), (sx, 0,  sz), (sx, sy, sz), (0,  sy, sz),
    ]
    faces = [
        (0, 1, 2, 3), (4, 5, 6, 7),
        (0, 1, 5, 4), (1, 2, 6, 5),
        (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    return _new_mesh_object(name, verts, faces)


def _empty_root(nombre, categoria):
    root = bpy.data.objects.new(nombre, None)
    root.empty_display_type = 'ARROWS'
    root["arch_categoria"] = categoria
    bpy.context.collection.objects.link(root)
    return root


def _set_meta(root, **params):
    """Guarda parámetros como propiedades ID (planas) y como JSON."""
    root["arch_params_json"] = json.dumps(params)
    for k, v in params.items():
        try:
            root[f"arch_{k}"] = float(v) if isinstance(v, (int, float)) else str(v)
        except Exception:
            root[f"arch_{k}"] = str(v)


def _parent(child, parent_obj):
    child.parent = parent_obj
    child.matrix_parent_inverse = Matrix.Identity(4)


def _apply_boolean(target_mesh, cutter_mesh, operation='DIFFERENCE'):
    """Aplica un modificador booleano y elimina el cutter."""
    mod = target_mesh.modifiers.new("_Bool_tmp", 'BOOLEAN')
    mod.operation = operation
    mod.solver = 'EXACT'
    mod.object = cutter_mesh
    bpy.context.view_layer.objects.active = target_mesh
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter_mesh, do_unlink=True)


# ---------------------------------------------------------
#  MATERIALES
# ---------------------------------------------------------

def asignar_material(obj, nombre="Mat",
                     base_color=(0.8, 0.8, 0.8, 1.0),
                     roughness=0.5, metallic=0.0,
                     transmission=0.0, ior=1.45):
    """
    Crea o reutiliza un material Principled BSDF y lo asigna al objeto.

    Args:
        obj: objeto Blender al que se asigna el material.
        nombre (str): nombre del material (se reutiliza si ya existe).
        base_color (tuple): RGBA en [0,1].
        roughness (float): rugosidad [0,1].
        metallic (float): metalicidad [0,1].
        transmission (float): transmisión (vidrio) [0,1].
        ior (float): índice de refracción.

    Returns:
        bpy.types.Material
    """
    mat = bpy.data.materials.get(nombre)
    if mat is None:
        mat = bpy.data.materials.new(nombre)
        mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = transmission
        elif "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        if "IOR" in bsdf.inputs:
            bsdf.inputs["IOR"].default_value = ior
    if obj.data and hasattr(obj.data, "materials"):
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
    return mat


# ---------------------------------------------------------
#  ELEMENTOS ESTRUCTURALES
# ---------------------------------------------------------

def crear_muro(nombre="Muro",
               largo=4.0, alto=3.0, grosor=0.2,
               origen=(0, 0, 0),
               rotacion_z=0.0,
               material="Muro_Generic"):
    """
    Crea un muro rectangular (prisma).
    Alineado a +X (largo), +Y (grosor), +Z (alto).

    Args:
        nombre (str): nombre del activo.
        largo (float): longitud en X (m).
        alto (float): altura en Z (m).
        grosor (float): grosor en Y (m).
        origen (tuple): posición (x, y, z) del root en coordenadas globales.
        rotacion_z (float): rotación en Z en grados (para muros oblicuos).
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "muro")
    root.location = Vector(origen)
    if rotacion_z:
        root.rotation_euler.z = radians(rotacion_z)
    muro = _box(f"{nombre}_Cuerpo", largo, grosor, alto)
    asignar_material(muro, material)
    _parent(muro, root)
    _set_meta(root, tipo="muro", largo=largo, alto=alto, grosor=grosor,
              origen=list(origen), rotacion_z=rotacion_z)
    return root


def crear_columna(nombre="Columna",
                  seccion="rect",
                  ancho=0.30, fondo=0.30, diametro=0.30,
                  alto=3.0,
                  origen=(0, 0, 0),
                  material="Hormigon"):
    """
    Crea una columna paramétrica con base en Z=0.

    Args:
        nombre (str): nombre del activo.
        seccion (str): 'rect' (rectangular) o 'circ' (circular).
        ancho (float): dimensión X para sección rectangular (m).
        fondo (float): dimensión Y para sección rectangular (m).
        diametro (float): diámetro para sección circular (m).
        alto (float): altura total (m).
        origen (tuple): posición (x, y, z).
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "columna")
    root.location = Vector(origen)

    if seccion.lower().startswith('c'):
        bm = bmesh.new()
        bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=False,
            segments=32,
            radius1=diametro / 2.0,
            radius2=diametro / 2.0,
            depth=alto,
        )
        # create_cone centra en Z=0 → trasladar para que base quede en Z=0
        bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, alto / 2.0))
        me = bpy.data.meshes.new(f"{nombre}_mesh")
        bm.to_mesh(me)
        bm.free()
        obj = bpy.data.objects.new(f"{nombre}_Cuerpo", me)
        bpy.context.collection.objects.link(obj)
    else:
        obj = _box(f"{nombre}_Cuerpo", ancho, fondo, alto)

    asignar_material(obj, material)
    _parent(obj, root)
    _set_meta(root, tipo="columna", seccion=seccion,
              ancho=ancho, fondo=fondo, diametro=diametro, alto=alto,
              origen=list(origen))
    return root


def crear_losa_rectangular(nombre="Losa",
                            ancho=4.0, fondo=3.0, espesor=0.20,
                            origen=(0, 0, 0),
                            material="Hormigon"):
    """
    Crea una losa rectangular (ancho X, fondo Y, espesor Z).

    Args:
        nombre (str): nombre del activo.
        ancho (float): dimensión X (m).
        fondo (float): dimensión Y (m).
        espesor (float): espesor en Z (m).
        origen (tuple): posición del root.
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = extruir_perfil(
        nombre=nombre,
        puntos_2d=((0, 0), (ancho, 0), (ancho, fondo), (0, fondo)),
        altura=espesor, cerrar_perfil=True, material=material,
    )
    root.location = Vector(origen)
    root["arch_categoria"] = "losa"
    _set_meta(root, tipo="losa", ancho=ancho, fondo=fondo,
              espesor=espesor, origen=list(origen))
    return root


def crear_piso(nombre="Piso",
               ancho=4.0, fondo=3.0, espesor=0.05,
               origen=(0, 0, 0),
               material="Suelo_Madera"):
    """
    Crea una losa de piso/suelo (versión delgada para interiores).
    Alias semántico de crear_losa_rectangular con espesor reducido.

    Args:
        nombre (str): nombre del activo.
        ancho (float): dimensión X (m).
        fondo (float): dimensión Y (m).
        espesor (float): espesor del acabado de piso (m). Default 5 cm.
        origen (tuple): posición (x, y, z).
        material (str): nombre del material (parquet, cerámica, etc.).

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = crear_losa_rectangular(nombre=nombre, ancho=ancho, fondo=fondo,
                                   espesor=espesor, origen=origen,
                                   material=material)
    root["arch_categoria"] = "piso"
    return root


def crear_techo_plano(nombre="TechoPlano",
                      ancho=6.0, fondo=4.0, espesor=0.20,
                      caida_x=0.0, caida_y=0.0,
                      origen=(0, 0, 3.0),
                      material="Losacero"):
    """
    Crea una losa/placa de techo con pendiente simple.

    Args:
        nombre (str): nombre del activo.
        ancho (float): dimensión X (m).
        fondo (float): dimensión Y (m).
        espesor (float): espesor de la losa (m).
        caida_x (float): ΔZ desde X=0 a X=ancho (positivo = baja hacia +X).
        caida_y (float): ΔZ desde Y=0 a Y=fondo.
        origen (tuple): posición (x, y, z) — z suele ser la cota de piso a techo.
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    z0 = origen[2]
    v0 = (0,     0,     z0)
    v1 = (ancho, 0,     z0)
    v2 = (ancho, fondo, z0)
    v3 = (0,     fondo, z0)
    v4 = (0,     0,     z0 + espesor)
    v5 = (ancho, 0,     z0 + espesor - caida_x)
    v6 = (ancho, fondo, z0 + espesor - caida_x - caida_y)
    v7 = (0,     fondo, z0 + espesor - caida_y)

    verts = [v0, v1, v2, v3, v4, v5, v6, v7]
    faces = [
        (0, 1, 2, 3), (4, 5, 6, 7),
        (0, 1, 5, 4), (1, 2, 6, 5),
        (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    placa = _new_mesh_object(f"{nombre}_Cuerpo", verts, faces)
    placa.location = Vector((origen[0], origen[1], 0))
    asignar_material(placa, material)
    root = _empty_root(nombre, "techo_plano")
    _parent(placa, root)
    _set_meta(root, tipo="techo_plano", ancho=ancho, fondo=fondo,
              espesor=espesor, caida_x=caida_x, caida_y=caida_y,
              origen=list(origen))
    return root


def crear_tejado_dos_aguas(nombre="Tejado",
                           ancho=8.0, fondo=6.0,
                           altura_cumbrera=2.5,
                           espesor=0.15,
                           voladizo_x=0.4, voladizo_y=0.3,
                           origen=(0, 0, 3.0),
                           material="Teja"):
    """
    Crea un tejado a dos aguas (gable roof) sobre una base rectangular.

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho total de la planta (X) sin voladizos (m).
        fondo (float): fondo total de la planta (Y) sin voladizos (m).
        altura_cumbrera (float): altura del caballete sobre el plano de arranque (m).
        espesor (float): grosor de los faldones (m).
        voladizo_x (float): vuelo en X más allá de la fachada (m).
        voladizo_y (float): vuelo en Y más allá de los hastiales (m).
        origen (tuple): posición (x, y, z) — z es la cota de arranque del tejado.
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "tejado_dos_aguas")
    root.location = Vector(origen)
    _set_meta(root, tipo="tejado_dos_aguas", ancho=ancho, fondo=fondo,
              altura_cumbrera=altura_cumbrera, espesor=espesor,
              voladizo_x=voladizo_x, voladizo_y=voladizo_y,
              origen=list(origen))

    ax = -voladizo_x
    bx = ancho + voladizo_x
    ay = -voladizo_y
    by = fondo + voladizo_y
    cx = ancho / 2.0  # X de la cumbrera

    import math
    
    # Alturas en Z inferior
    z_alero = - voladizo_x * (altura_cumbrera / (ancho / 2.0))
    z_cumbrera = altura_cumbrera
    
    # Alturas en Z superior
    dz = espesor / math.cos(math.atan2(altura_cumbrera, ancho / 2.0))
    
    verts = [
        (ax, ay, z_alero), (cx, ay, z_cumbrera), (bx, ay, z_alero),
        (ax, by, z_alero), (cx, by, z_cumbrera), (bx, by, z_alero),
        (ax, ay, z_alero + dz), (cx, ay, z_cumbrera + dz), (bx, ay, z_alero + dz),
        (ax, by, z_alero + dz), (cx, by, z_cumbrera + dz), (bx, by, z_alero + dz),
    ]
    
    faces = [
        # Faldon izquierdo
        (0, 1, 4, 3), # inferior
        (6, 7, 10, 9), # superior
        (0, 3, 9, 6), # extremo
        (0, 6, 7, 1), # front
        (3, 4, 10, 9), # back
        # Faldon derecho
        (1, 2, 5, 4), # inferior
        (7, 8, 11, 10), # superior
        (2, 8, 11, 5), # extremo
        (1, 7, 8, 2), # front
        (4, 5, 11, 10) # back
    ]
    
    me = _new_mesh_object(f"{nombre}_Cuerpo", verts, faces)
    asignar_material(me, material)
    _parent(me, root)

    return root


# ---------------------------------------------------------
#  HUECOS Y ABERTURAS
# ---------------------------------------------------------

def crear_ventana(nombre="Ventana",
                  ancho=1.2, alto=1.2,
                  espesor_marco=0.06, prof_marco=0.08,
                  divisiones=(1, 1), espesor_divisor=0.03,
                  espesor_vidrio=0.006, retranqueo_vidrio=0.02,
                  origen=(0, 0, 0),
                  material_marco="Marco_Pintura",
                  material_vidrio="Vidrio"):
    """
    Crea una ventana paramétrica (marco + divisiones + vidrios).
    Origen en esquina inferior-trasera (0,0,0).
    Extiende +X (ancho), +Y (prof_marco), +Z (alto).

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho total (m).
        alto (float): altura total (m).
        espesor_marco (float): grosor del perfil del marco (m).
        prof_marco (float): profundidad del marco (m).
        divisiones (tuple): (nx, ny) — columnas x filas de paños.
        espesor_divisor (float): grosor del travesaño/montante (m).
        espesor_vidrio (float): grosor del vidrio (m).
        retranqueo_vidrio (float): retranqueo del vidrio respecto al marco (m).
        origen (tuple): posición (x, y, z) del root.
        material_marco (str): nombre del material del marco.
        material_vidrio (str): nombre del material del vidrio.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    nx, ny = max(1, int(divisiones[0])), max(1, int(divisiones[1]))
    clear_w = max(0.01, ancho - 2 * espesor_marco)
    clear_h = max(0.01, alto  - 2 * espesor_marco)
    root = _empty_root(nombre, "ventana")
    root.location = Vector(origen)
    _set_meta(root, tipo="ventana", ancho=ancho, alto=alto,
              espesor_marco=espesor_marco, prof_marco=prof_marco,
              nx=nx, ny=ny, espesor_divisor=espesor_divisor,
              espesor_vidrio=espesor_vidrio, origen=list(origen))

    j_izq = _box(f"{nombre}_Jamba_Izq", espesor_marco, prof_marco, alto)
    j_der = _box(f"{nombre}_Jamba_Der", espesor_marco, prof_marco, alto)
    j_der.location.x = ancho - espesor_marco
    t_inf = _box(f"{nombre}_Trav_Inf", clear_w, prof_marco, espesor_marco)
    t_inf.location = Vector((espesor_marco, 0, 0))
    t_sup = _box(f"{nombre}_Trav_Sup", clear_w, prof_marco, espesor_marco)
    t_sup.location = Vector((espesor_marco, 0, alto - espesor_marco))
    for p in (j_izq, j_der, t_inf, t_sup):
        asignar_material(p, material_marco)
        _parent(p, root)

    # montantes verticales
    if nx > 1:
        paso = clear_w / nx
        for i in range(1, nx):
            x = espesor_marco + i * paso - espesor_divisor / 2.0
            mull = _box(f"{nombre}_Mul_V_{i}", espesor_divisor, prof_marco, clear_h)
            mull.location = Vector((x, 0, espesor_marco))
            asignar_material(mull, material_marco)
            _parent(mull, root)

    # travesaños horizontales
    if ny > 1:
        paso = clear_h / ny
        for j in range(1, ny):
            z = espesor_marco + j * paso - espesor_divisor / 2.0
            mull = _box(f"{nombre}_Mul_H_{j}", clear_w, prof_marco, espesor_divisor)
            mull.location = Vector((espesor_marco, 0, z))
            asignar_material(mull, material_marco)
            _parent(mull, root)

    # crear material de vidrio una sola vez
    _tmp = _box(f"{nombre}_V_TMP", 0.01, 0.01, 0.01)
    vidrio_mat = asignar_material(
        _tmp, material_vidrio,
        base_color=(0.7, 0.85, 1.0, 1.0),
        roughness=0.05, metallic=0.0, transmission=1.0, ior=1.45,
    )
    bpy.data.objects.remove(_tmp, do_unlink=True)

    pane_w = (clear_w - (nx - 1) * espesor_divisor) / nx
    pane_h = (clear_h - (ny - 1) * espesor_divisor) / ny
    for ix in range(nx):
        for iy in range(ny):
            x = espesor_marco + ix * (pane_w + espesor_divisor)
            z = espesor_marco + iy * (pane_h + espesor_divisor)
            panel = _box(
                f"{nombre}_Vidrio_{ix+1}_{iy+1}",
                pane_w,
                max(0.002, prof_marco - retranqueo_vidrio),
                pane_h,
            )
            panel.location = Vector((x, retranqueo_vidrio, z))
            panel.data.materials.append(vidrio_mat)
            _parent(panel, root)

    return root


def crear_puerta(nombre="Puerta",
                 ancho=0.9, alto=2.1,
                 espesor_panel=0.04,
                 ancho_marco=0.08, prof_marco=0.1,
                 holgura=0.005,
                 origen=(0, 0, 0),
                 material_panel="Madera",
                 material_marco="Marco_Pintura"):
    """
    Crea una puerta batiente simple (panel + marco U).
    Origen en esquina inferior-trasera del marco.

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho total con marco (m).
        alto (float): altura total con marco (m).
        espesor_panel (float): grosor de la hoja (m).
        ancho_marco (float): ancho del perfil del marco (m).
        prof_marco (float): profundidad del marco (m).
        holgura (float): espacio libre entre panel y marco (m).
        origen (tuple): posición (x, y, z) del root.
        material_panel (str): nombre del material de la hoja.
        material_marco (str): nombre del material del marco.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "puerta")
    root.location = Vector(origen)
    _set_meta(root, tipo="puerta", ancho=ancho, alto=alto,
              espesor_panel=espesor_panel, ancho_marco=ancho_marco,
              prof_marco=prof_marco, origen=list(origen))

    j_izq  = _box(f"{nombre}_Jamba_Izq", ancho_marco, prof_marco, alto)
    j_der  = _box(f"{nombre}_Jamba_Der", ancho_marco, prof_marco, alto)
    j_der.location.x = ancho - ancho_marco
    dintel = _box(f"{nombre}_Dintel", ancho - 2 * ancho_marco, prof_marco, ancho_marco)
    dintel.location = Vector((ancho_marco, 0, alto - ancho_marco))
    for p in (j_izq, j_der, dintel):
        asignar_material(p, material_marco)
        _parent(p, root)

    clear_w = ancho - 2 * ancho_marco - 2 * holgura
    clear_h = alto  - ancho_marco     - 2 * holgura
    panel   = _box(f"{nombre}_Panel", clear_w, espesor_panel, clear_h)
    panel.location = Vector((
        ancho_marco + holgura,
        (prof_marco - espesor_panel) / 2.0,
        holgura,
    ))
    asignar_material(panel, material_panel)
    _parent(panel, root)
    return root


def abrir_vanos_batch_rectangulares(muro, centros_world,
                                    ancho=1.2, alto=1.2,
                                    profundidad=None,
                                    aplicar=True,
                                    nombre="VanosBatch"):
    """
    Abre múltiples huecos rectangulares en un muro con UNA sola operación
    booleana (más eficiente que una operación por vano).

    Args:
        muro: root (Empty) o MESH del muro.
        centros_world (list): lista de tuplas (x, y, z) — centros de cada
            vano en coordenadas globales.
        ancho (float): ancho del hueco (m).
        alto (float): altura del hueco (m).
        profundidad (float|None): si None, usa el grosor del muro × 1.05.
        aplicar (bool): si True, aplica el modificador y elimina el cutter.
        nombre (str): prefijo para los objetos cutter.

    Returns:
        bpy.types.Object: el MESH del muro con los vanos abiertos.

    """
    muro_mesh = _first_mesh_child(muro)
    ys = [v[1] for v in muro_mesh.bound_box]
    grosor_local = (max(ys) - min(ys)) if ys else 0.2
    prof = profundidad if profundidad else grosor_local * 1.05

    M    = muro_mesh.matrix_world
    Minv = M.inverted()
    cutters = []
    for i, c in enumerate(centros_world, 1):
        pos_local = Minv @ Vector(c)
        cutter = _box(f"{nombre}_cutter_{i}", ancho, prof, alto)
        offset = Matrix.Translation(
            pos_local - Vector((ancho / 2.0, prof / 2.0, alto / 2.0))
        )
        cutter.matrix_world = M @ offset
        cutters.append(cutter)

    if not cutters:
        return muro_mesh

    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = cutters[0]
    for c in cutters:
        c.select_set(True)
    bpy.ops.object.join()
    cutter_union = bpy.context.active_object
    cutter_union.name = f"{nombre}_Union"

    bool_mod = muro_mesh.modifiers.new(f"{nombre}_Bool", 'BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.solver    = 'EXACT'
    bool_mod.object    = cutter_union
    bpy.context.view_layer.objects.active = muro_mesh
    if aplicar:
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)
        bpy.data.objects.remove(cutter_union, do_unlink=True)
    return muro_mesh


def abrir_vanos_grid_local(muro, filas=3, cols=4,
                           x0=1.2, z0=1.2, dx=1.8, dz=3.0,
                           ancho=1.2, alto=1.2,
                           profundidad=None,
                           nombre="VanosGrid",
                           aplicar=True):
    """
    Genera una rejilla (filas × columnas) de vanos en el sistema local del muro.

    Args:
        muro: root o MESH del muro.
        filas (int): número de filas.
        cols (int): número de columnas.
        x0, z0 (float): centro del primer vano en local (m).
        dx, dz (float): separación entre centros en local (m).
        ancho, alto (float): dimensiones de cada vano (m).
        profundidad (float|None): profundidad del corte.
        nombre (str): prefijo para objetos auxiliares.
        aplicar (bool): aplicar booleano.

    Returns:
        bpy.types.Object: MESH del muro con los vanos abiertos.

    """
    muro_mesh = _first_mesh_child(muro)
    ys        = [v[1] for v in muro_mesh.bound_box]
    yctr      = (min(ys) + max(ys)) / 2.0
    M         = muro_mesh.matrix_world
    centros   = [
        tuple(M @ Vector((x0 + c * dx, yctr, z0 + r * dz)))
        for r in range(filas)
        for c in range(cols)
    ]
    return abrir_vanos_batch_rectangulares(
        muro_mesh, centros, ancho, alto, profundidad, aplicar, nombre
    )


# ---------------------------------------------------------
#  ESCALERAS Y CIRCULACIÓN
# ---------------------------------------------------------

def crear_escalera_recta(nombre="Escalera",
                         huella=0.28, contrahuella=0.175,
                         ancho=1.1, num_peldanos=16,
                         grosor_peldano=0.03,
                         con_contrahuellas=True,
                         con_zancas=True, espesor_zanca=0.15,
                         origen=(0, 0, 0),
                         material="Hormigon"):
    """
    Crea una escalera recta paramétrica con peldaños, contrahuellas
    opcionales y zancas laterales.

    Args:
        nombre (str): nombre del activo.
        huella (float): profundidad del peldaño (m).
        contrahuella (float): altura del escalón (m).
        ancho (float): ancho libre entre zancas (m).
        num_peldanos (int): número de escalones.
        grosor_peldano (float): espesor del tablero de la huella (m).
        con_contrahuellas (bool): añadir panel frontal (contrahuella).
        con_zancas (bool): añadir zancas laterales.
        espesor_zanca (float): grosor de cada zanca lateral (m).
        origen (tuple): posición (x, y, z) del primer peldaño.
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "escalera_recta")
    root.location = Vector(origen)
    _set_meta(root, tipo="escalera_recta",
              huella=huella, contrahuella=contrahuella,
              ancho=ancho, num_peldanos=num_peldanos,
              grosor_peldano=grosor_peldano,
              con_contrahuellas=con_contrahuellas,
              con_zancas=con_zancas)

    ancho_util = ancho  # sin zancas
    off_y = espesor_zanca if con_zancas else 0.0

    for i in range(num_peldanos):
        x = i * huella
        z = i * contrahuella
        # huella (tablero horizontal)
        h = _box(f"{nombre}_Huella_{i+1}", huella, ancho_util, grosor_peldano)
        h.location = Vector((x, off_y, z + contrahuella - grosor_peldano))
        asignar_material(h, material)
        _parent(h, root)
        # contrahuella (panel vertical frontal)
        if con_contrahuellas and i < num_peldanos:
            ch = _box(f"{nombre}_CH_{i+1}", grosor_peldano, ancho_util, contrahuella)
            ch.location = Vector((x, off_y, z))
            asignar_material(ch, material)
            _parent(ch, root)

    # zancas laterales (vigas inclinadas que soportan la escalera)
    if con_zancas:
        largo_total = num_peldanos * huella
        alto_total  = num_peldanos * contrahuella
        for side_y in (0.0, ancho_util + espesor_zanca):
            pts = [
                (0,           0, 0),
                (largo_total, 0, alto_total - contrahuella),
                (largo_total, 0, alto_total),
                (0,           0, contrahuella)
            ]
            bm = bmesh.new()
            v_list = [bm.verts.new(p) for p in pts]
            bm.verts.ensure_lookup_table()
            bm.faces.new(v_list)
            bm.faces.ensure_lookup_table()
            ex = bmesh.ops.extrude_face_region(bm, geom=[bm.faces[0]])
            bmesh.ops.translate(
                bm, vec=(0, espesor_zanca, 0),
                verts=[v for v in ex["geom"] if isinstance(v, bmesh.types.BMVert)]
            )
            me = bpy.data.meshes.new(f"{nombre}_Zanca_mesh")
            bm.to_mesh(me)
            bm.free()
            zanca = bpy.data.objects.new(f"{nombre}_Zanca_{int(side_y)}", me)
            bpy.context.collection.objects.link(zanca)
            zanca.location.y = side_y
            zanca.location.x = 0
            asignar_material(zanca, material)
            _parent(zanca, root)

    return root


def crear_baranda_lineal(nombre="Baranda",
                         largo=4.0, altura=1.0,
                         poste_cada=1.2,
                         seccion_poste=0.04,
                         seccion_pasamanos=(0.04, 0.08),
                         num_travesanos=2,
                         origen=(0, 0, 0),
                         material="Metal"):
    """
    Baranda lineal a lo largo de +X con postes y pasamanos.

    Args:
        nombre (str): nombre del activo.
        largo (float): longitud total en X (m).
        altura (float): altura total de la baranda (m).
        poste_cada (float): distancia entre postes (m).
        seccion_poste (float): sección cuadrada del poste (m).
        seccion_pasamanos (tuple): (grosor_X, grosor_Y) del pasamanos (m).
        num_travesanos (int): número de travesaños horizontales intermedios.
        origen (tuple): posición (x, y, z) del root.
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "baranda")
    root.location = Vector(origen)
    _set_meta(root, tipo="baranda", largo=largo, altura=altura,
              poste_cada=poste_cada, num_travesanos=num_travesanos)

    n_postes = max(2, int(largo / poste_cada) + 1)
    step     = largo / (n_postes - 1)
    for i in range(n_postes):
        post = _box(f"{nombre}_Poste_{i+1}", seccion_poste, seccion_poste, altura)
        post.location = Vector((i * step, 0, 0))
        asignar_material(post, material)
        _parent(post, root)

    pw, py = seccion_pasamanos
    # pasamanos superior
    top = _box(f"{nombre}_Top", largo, py, pw)
    top.location = Vector((0, 0, altura - pw))
    asignar_material(top, material)
    _parent(top, root)

    # travesaños intermedios
    for t in range(1, num_travesanos + 1):
        z_t = altura * t / (num_travesanos + 1)
        trav = _box(f"{nombre}_Trav_{t}", largo, py, pw)
        trav.location = Vector((0, 0, z_t))
        asignar_material(trav, material)
        _parent(trav, root)

    return root


# ---------------------------------------------------------
#  MOBILIARIO INTERIOR
# ---------------------------------------------------------

def crear_mesa(nombre="Mesa",
               ancho=1.6, fondo=0.8, alto=0.75,
               grosor_tablero=0.04, espesor_pata=0.05,
               setback_pata=0.06,
               origen=(0, 0, 0),
               material_tablero="Madera",
               material_patas="Metal"):
    """
    Crea una mesa rectangular con 4 patas.

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho del tablero en X (m).
        fondo (float): fondo del tablero en Y (m).
        alto (float): altura total de la mesa (m).
        grosor_tablero (float): espesor del tablero (m).
        espesor_pata (float): sección cuadrada de cada pata (m).
        setback_pata (float): retranqueo de la pata respecto al borde (m).
        origen (tuple): posición (x, y, z).
        material_tablero (str): nombre del material del tablero.
        material_patas (str): nombre del material de las patas.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "mesa")
    root.location = Vector(origen)
    _set_meta(root, tipo="mesa", ancho=ancho, fondo=fondo, alto=alto,
              grosor_tablero=grosor_tablero, espesor_pata=espesor_pata)

    tablero = _box(f"{nombre}_Tablero", ancho, fondo, grosor_tablero)
    tablero.location = Vector((0, 0, alto - grosor_tablero))
    asignar_material(tablero, material_tablero)
    _parent(tablero, root)

    for dx in (setback_pata, ancho - setback_pata - espesor_pata):
        for dy in (setback_pata, fondo - setback_pata - espesor_pata):
            pata = _box(f"{nombre}_Pata", espesor_pata, espesor_pata,
                        alto - grosor_tablero)
            pata.location = Vector((dx, dy, 0))
            asignar_material(pata, material_patas)
            _parent(pata, root)
    return root


def crear_silla(nombre="Silla",
                ancho=0.45, fondo=0.45,
                alto_asiento=0.45, alto_respaldo=0.9,
                grosor=0.03,
                origen=(0, 0, 0),
                material="Madera"):
    """
    Crea una silla con 4 patas, asiento y respaldo.

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho del asiento (m).
        fondo (float): fondo del asiento (m).
        alto_asiento (float): altura del asiento desde el suelo (m).
        alto_respaldo (float): altura total del respaldo desde el suelo (m).
        grosor (float): sección cuadrada de patas y tableros (m).
        origen (tuple): posición (x, y, z).
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.
    """
    root = _empty_root(nombre, "silla")
    root.location = Vector(origen)
    _set_meta(root, tipo="silla", ancho=ancho, fondo=fondo,
              alto_asiento=alto_asiento, alto_respaldo=alto_respaldo)

    for dx in (0, ancho - grosor):
        for dy in (0, fondo - grosor):
            pata = _box(f"{nombre}_Pata", grosor, grosor, alto_asiento)
            pata.location = Vector((dx, dy, 0))
            asignar_material(pata, material)
            _parent(pata, root)

    asiento = _box(f"{nombre}_Asiento", ancho, fondo, grosor)
    asiento.location = Vector((0, 0, alto_asiento))
    asignar_material(asiento, material)
    _parent(asiento, root)

    respaldo = _box(f"{nombre}_Respaldo", grosor, fondo,
                    max(0.01, alto_respaldo - alto_asiento))
    respaldo.location = Vector((0, 0, alto_asiento))
    asignar_material(respaldo, material)
    _parent(respaldo, root)
    return root


def crear_sofa(nombre="Sofa",
               ancho=2.0, fondo=0.9,
               alto_asiento=0.45, alto_respaldo=0.85,
               ancho_brazo=0.12, grosor=0.1,
               origen=(0, 0, 0),
               material="Tela",
               material_estructura="Madera"):
    """
    Crea un sofá (base + cojín de asiento + respaldo + brazos).

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho total con brazos (m).
        fondo (float): fondo total (m).
        alto_asiento (float): altura de la superficie del asiento (m).
        alto_respaldo (float): altura total del respaldo (m).
        ancho_brazo (float): ancho de cada brazo lateral (m).
        grosor (float): grosor de la base (m).
        origen (tuple): posición (x, y, z).
        material (str): material de tapizado.
        material_estructura (str): material de la estructura.

    Returns:
        bpy.types.Object: root (Empty) del activo.
    """
    root = _empty_root(nombre, "sofa")
    root.location = Vector(origen)
    _set_meta(root, tipo="sofa", ancho=ancho, fondo=fondo,
              alto_asiento=alto_asiento, alto_respaldo=alto_respaldo)

    base = _box(f"{nombre}_Base", ancho, fondo, grosor)
    asignar_material(base, material_estructura)
    _parent(base, root)

    coj = _box(f"{nombre}_Cojin", ancho - 2 * 0.04, fondo - 2 * 0.04, 0.12)
    coj.location = Vector((0.02, 0.02, grosor))
    asignar_material(coj, material)
    _parent(coj, root)

    res = _box(f"{nombre}_Respaldo",
               ancho - 2 * ancho_brazo, grosor,
               alto_respaldo - alto_asiento)
    res.location = Vector((ancho_brazo, fondo - grosor, alto_asiento))
    asignar_material(res, material)
    _parent(res, root)

    b1 = _box(f"{nombre}_Brazo_Izq", ancho_brazo, fondo, alto_respaldo)
    b2 = _box(f"{nombre}_Brazo_Der", ancho_brazo, fondo, alto_respaldo)
    b2.location.x = ancho - ancho_brazo
    for b in (b1, b2):
        asignar_material(b, material_estructura)
        _parent(b, root)
    return root


def crear_cama(nombre="Cama",
               ancho=1.6, largo=2.0,
               alto_base=0.35, alto_cabecero=1.0,
               grosor_base=0.06, grosor_colchon=0.25,
               origen=(0, 0, 0),
               material_base="Madera",
               material_colchon="Textil"):
    """
    Crea una cama con base, colchón y cabecero.

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho de la cama en X (m). Simple=0.9, Doble=1.6, Queen=1.6, King=2.0.
        largo (float): largo de la cama en Y (m).
        alto_base (float): altura de la base desde el suelo (m).
        alto_cabecero (float): altura del cabecero desde el suelo (m).
        grosor_base (float): espesor del tablero de la base (m).
        grosor_colchon (float): grosor del colchón (m).
        origen (tuple): posición (x, y, z).
        material_base (str): material de la base y cabecero.
        material_colchon (str): material del colchón.

    Returns:
        bpy.types.Object: root (Empty) del activo.
    """
    root = _empty_root(nombre, "cama")
    root.location = Vector(origen)
    _set_meta(root, tipo="cama", ancho=ancho, largo=largo,
              alto_base=alto_base, alto_cabecero=alto_cabecero)

    base = _box(f"{nombre}_Base", ancho, largo, grosor_base)
    asignar_material(base, material_base)
    _parent(base, root)

    colchon = _box(f"{nombre}_Colchon", ancho - 0.04, largo - 0.04, grosor_colchon)
    colchon.location = Vector((0.02, 0.02, grosor_base))
    asignar_material(colchon, material_colchon)
    _parent(colchon, root)

    cab = _box(f"{nombre}_Cabecero", ancho, 0.06, max(0.01, alto_cabecero - alto_base))
    cab.location = Vector((0, 0, alto_base))
    asignar_material(cab, material_base)
    _parent(cab, root)
    return root


def crear_estanteria(nombre="Estanteria",
                     ancho=1.2, alto=2.0, fondo=0.35,
                     num_estantes=5, grosor_tablero=0.025,
                     grosor_lateral=0.02,
                     con_fondo=True,
                     origen=(0, 0, 0),
                     material="Madera"):
    """
    Crea una estantería/librero con tableros horizontales y laterales.

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho total exterior (m).
        alto (float): altura total exterior (m).
        fondo (float): profundidad (m).
        num_estantes (int): número de estantes interiores (sin contar base y tapa).
        grosor_tablero (float): grosor de cada tablero horizontal (m).
        grosor_lateral (float): grosor de los tableros laterales (m).
        con_fondo (bool): si True, añade panel trasero delgado.
        origen (tuple): posición (x, y, z).
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "estanteria")
    root.location = Vector(origen)
    _set_meta(root, tipo="estanteria", ancho=ancho, alto=alto, fondo=fondo,
              num_estantes=num_estantes, grosor_tablero=grosor_tablero)

    # laterales
    lat_izq = _box(f"{nombre}_Lat_Izq", grosor_lateral, fondo, alto)
    lat_der = _box(f"{nombre}_Lat_Der", grosor_lateral, fondo, alto)
    lat_der.location.x = ancho - grosor_lateral
    for lat in (lat_izq, lat_der):
        asignar_material(lat, material)
        _parent(lat, root)

    ancho_int = ancho - 2 * grosor_lateral
    # base y tapa
    for z_t, tag in ((0, "Base"), (alto - grosor_tablero, "Tapa")):
        t = _box(f"{nombre}_{tag}", ancho_int, fondo, grosor_tablero)
        t.location = Vector((grosor_lateral, 0, z_t))
        asignar_material(t, material)
        _parent(t, root)

    # estantes intermedios
    espacio_total = alto - 2 * grosor_tablero
    paso = espacio_total / (num_estantes + 1)
    for i in range(1, num_estantes + 1):
        z_e = grosor_tablero + i * paso - grosor_tablero / 2
        est = _box(f"{nombre}_Estante_{i}", ancho_int, fondo, grosor_tablero)
        est.location = Vector((grosor_lateral, 0, z_e))
        asignar_material(est, material)
        _parent(est, root)

    # fondo (panel trasero)
    if con_fondo:
        fondo_panel = _box(f"{nombre}_Fondo", ancho, 0.01, alto)
        fondo_panel.location = Vector((0, fondo - 0.01, 0))
        asignar_material(fondo_panel, material)
        _parent(fondo_panel, root)

    return root


def crear_armario(nombre="Armario",
                  ancho=1.8, alto=2.4, fondo=0.6,
                  num_puertas=2, grosor_cuerpo=0.02,
                  grosor_puerta=0.02,
                  con_zocalo=True, alto_zocalo=0.1,
                  origen=(0, 0, 0),
                  material_cuerpo="Madera",
                  material_puerta="Madera_Lacada"):
    """
    Crea un armario/closet con cuerpo (caja) y puertas batientes.

    Args:
        nombre (str): nombre del activo.
        ancho (float): ancho total exterior (m).
        alto (float): altura total exterior (m).
        fondo (float): profundidad (m).
        num_puertas (int): número de puertas (1–4).
        grosor_cuerpo (float): grosor de los tableros del cuerpo (m).
        grosor_puerta (float): grosor de cada hoja de puerta (m).
        con_zocalo (bool): añadir zócalo inferior.
        alto_zocalo (float): altura del zócalo (m).
        origen (tuple): posición (x, y, z).
        material_cuerpo (str): material del cuerpo.
        material_puerta (str): material de las puertas.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "armario")
    root.location = Vector(origen)
    _set_meta(root, tipo="armario", ancho=ancho, alto=alto, fondo=fondo,
              num_puertas=num_puertas)

    z0 = alto_zocalo if con_zocalo else 0.0
    alto_cuerpo = alto - z0

    # cuerpo (6 caras)
    partes = [
        (_box(f"{nombre}_Lat_Izq", grosor_cuerpo, fondo, alto_cuerpo),
         (0, 0, z0)),
        (_box(f"{nombre}_Lat_Der", grosor_cuerpo, fondo, alto_cuerpo),
         (ancho - grosor_cuerpo, 0, z0)),
        (_box(f"{nombre}_Base", ancho, fondo, grosor_cuerpo),
         (0, 0, z0)),
        (_box(f"{nombre}_Tapa", ancho, fondo, grosor_cuerpo),
         (0, 0, alto - grosor_cuerpo)),
        (_box(f"{nombre}_Fondo", ancho, grosor_cuerpo, alto_cuerpo),
         (0, fondo - grosor_cuerpo, z0)),
    ]
    for obj, loc in partes:
        obj.location = Vector(loc)
        asignar_material(obj, material_cuerpo)
        _parent(obj, root)

    # zócalo
    if con_zocalo:
        zoc = _box(f"{nombre}_Zocalo", ancho, fondo - 0.05, alto_zocalo)
        zoc.location = Vector((0, 0.05, 0))
        asignar_material(zoc, material_cuerpo)
        _parent(zoc, root)

    # puertas
    ancho_int = ancho - 2 * grosor_cuerpo
    ancho_puerta = ancho_int / num_puertas
    alto_puerta  = alto_cuerpo - grosor_cuerpo * 2 - 0.005
    for i in range(num_puertas):
        x_p = grosor_cuerpo + i * ancho_puerta + 0.002
        puerta = _box(f"{nombre}_Puerta_{i+1}",
                      ancho_puerta - 0.004, grosor_puerta, alto_puerta)
        puerta.location = Vector((x_p, 0, z0 + grosor_cuerpo + 0.002))
        asignar_material(puerta, material_puerta)
        _parent(puerta, root)

    return root


# ---------------------------------------------------------
#  ELEMENTOS EXTERIORES
# ---------------------------------------------------------

def crear_terreno_plano(nombre="Terreno",
                        ancho=20.0, fondo=15.0, espesor=0.3,
                        origen=(0, 0, -0.3),
                        material="Tierra"):
    """
    Crea una plataforma de terreno/sitio para escenas exteriores.

    Args:
        nombre (str): nombre del activo.
        ancho (float): dimensión X (m).
        fondo (float): dimensión Y (m).
        espesor (float): profundidad del volumen (m).
        origen (tuple): posición (x, y, z) — z suele ser negativo.
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "terreno")
    root.location = Vector(origen)
    terreno = _box(f"{nombre}_Cuerpo", ancho, fondo, espesor)
    asignar_material(terreno, material,
                     base_color=(0.25, 0.18, 0.10, 1.0), roughness=0.9)
    _parent(terreno, root)
    _set_meta(root, tipo="terreno", ancho=ancho, fondo=fondo,
              espesor=espesor, origen=list(origen))
    return root


def crear_arbol_simple(nombre="Arbol",
                       radio_copa=1.5, altura_copa=3.0,
                       altura_tronco=1.5, radio_tronco=0.12,
                       origen=(0, 0, 0),
                       material_tronco="Madera_Tronco",
                       material_copa="Follaje"):
    """
    Crea un árbol esquemático (tronco cilíndrico + copa esférica/cónica).
    Útil como placeholder en escenas exteriores.

    Args:
        nombre (str): nombre del activo.
        radio_copa (float): radio de la copa (m).
        altura_copa (float): altura del volumen de copa (m).
        altura_tronco (float): altura del tronco (m).
        radio_tronco (float): radio del tronco (m).
        origen (tuple): posición base del árbol (x, y, z).
        material_tronco (str): material del tronco.
        material_copa (str): material de la copa.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "arbol")
    root.location = Vector(origen)
    _set_meta(root, tipo="arbol", radio_copa=radio_copa,
              altura_tronco=altura_tronco, radio_tronco=radio_tronco)

    # tronco
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12,
                          radius1=radio_tronco, radius2=radio_tronco * 0.7,
                          depth=altura_tronco)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, altura_tronco / 2.0))
    me_t = bpy.data.meshes.new(f"{nombre}_Tronco_mesh")
    bm.to_mesh(me_t)
    bm.free()
    tronco = bpy.data.objects.new(f"{nombre}_Tronco", me_t)
    bpy.context.collection.objects.link(tronco)
    asignar_material(tronco, material_tronco,
                     base_color=(0.28, 0.18, 0.10, 1.0), roughness=0.9)
    _parent(tronco, root)

    # copa (cono invertido simplificado)
    bm2 = bmesh.new()
    bmesh.ops.create_cone(bm2, cap_ends=True, cap_tris=False, segments=16,
                          radius1=radio_copa, radius2=0.1,
                          depth=altura_copa)
    bmesh.ops.translate(bm2, verts=bm2.verts,
                        vec=(0, 0, altura_tronco + altura_copa / 2.0))
    me_c = bpy.data.meshes.new(f"{nombre}_Copa_mesh")
    bm2.to_mesh(me_c)
    bm2.free()
    copa = bpy.data.objects.new(f"{nombre}_Copa", me_c)
    bpy.context.collection.objects.link(copa)
    asignar_material(copa, material_copa,
                     base_color=(0.10, 0.35, 0.12, 1.0), roughness=0.8)
    _parent(copa, root)

    return root


# ---------------------------------------------------------
#  COMPOSITES DE ALTO NIVEL
# ---------------------------------------------------------

def crear_habitacion(nombre="Habitacion",
                     ancho=5.0, fondo=4.0, alto=3.0,
                     grosor_muro=0.2, grosor_losa=0.2,
                     con_suelo=True, con_techo=True,
                     origen=(0, 0, 0),
                     material_muro="Muro_Generic",
                     material_suelo="Suelo_Madera",
                     material_techo="Losacero"):
    """
    Crea una habitación completa: 4 muros perimetrales + suelo + techo.
    Los muros se crean en sentido horario: Sur (+X), Este (+Y),
    Norte (−X), Oeste (−Y).

    Args:
        nombre (str): nombre del activo raíz.
        ancho (float): dimensión interior X (m).
        fondo (float): dimensión interior Y (m).
        alto (float): altura interior (m).
        grosor_muro (float): grosor de muros (m).
        grosor_losa (float): grosor de suelo y techo (m).
        con_suelo (bool): generar losa de suelo.
        con_techo (bool): generar losa de techo.
        origen (tuple): posición (x, y, z) de la esquina interior inferior.
        material_muro (str): material de los muros.
        material_suelo (str): material del suelo.
        material_techo (str): material del techo.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    root = _empty_root(nombre, "habitacion")
    root.location = Vector(origen)
    _set_meta(root, tipo="habitacion", ancho=ancho, fondo=fondo,
              alto=alto, grosor_muro=grosor_muro)

    g = grosor_muro
    # muro Sur  (Y=−g, orientado +X)
    m_s = crear_muro(f"{nombre}_Muro_Sur",
                     largo=ancho + 2*g, alto=alto, grosor=g,
                     origen=(0, 0, 0), material=material_muro)
    # muro Norte (Y=fondo, orientado +X)
    m_n = crear_muro(f"{nombre}_Muro_Norte",
                     largo=ancho + 2*g, alto=alto, grosor=g,
                     origen=(0, fondo + g, 0), material=material_muro)
    # muro Oeste (X=−g, orientado +Y)
    m_o = crear_muro(f"{nombre}_Muro_Oeste",
                     largo=fondo, alto=alto, grosor=g,
                     origen=(0, g, 0), rotacion_z=90,
                     material=material_muro)
    # muro Este  (X=ancho+g, orientado +Y)
    m_e = crear_muro(f"{nombre}_Muro_Este",
                     largo=fondo, alto=alto, grosor=g,
                     origen=(ancho + g, g, 0), rotacion_z=90,
                     material=material_muro)

    for m in (m_s, m_n, m_o, m_e):
        _parent(m, root)

    if con_suelo:
        suelo = crear_piso(f"{nombre}_Suelo",
                           ancho=ancho, fondo=fondo,
                           espesor=grosor_losa,
                           origen=(g, g, -grosor_losa),
                           material=material_suelo)
        _parent(suelo, root)

    if con_techo:
        techo = crear_techo_plano(f"{nombre}_Techo",
                                  ancho=ancho, fondo=fondo,
                                  espesor=grosor_losa,
                                  origen=(g, g, alto),
                                  material=material_techo)
        _parent(techo, root)

    return root


def crear_casa_n_pisos(nombre="Casa",
                       pisos=2,
                       ancho=10.0,
                       fondo=8.0,
                       alto_piso=2.80,
                       grosor_muro=0.20,
                       grosor_losa=0.20,
                       con_tejado=True,
                       altura_cumbrera=1.50,
                       voladizo=0.40,
                       origen=(0, 0, 0),
                       material_muro="Muro_Pintura",
                       material_losa="Hormigon",
                       material_tejado="Teja"):
    """
    Genera una casa residencial de N pisos: envolvente de muros + losas
    apiladas verticalmente y tejado a dos aguas opcional en la última planta.

    Cada piso es una caja cerrada (4 muros + losa de techo que es también
    el suelo del piso siguiente). El primer piso no genera losa de suelo
    propia; se asume que la cimentación o el terreno lo resuelven.

    Args:
        nombre (str): nombre del activo raíz.
        pisos (int): número de plantas (≥ 1).
        ancho (float): dimensión exterior X (m).
        fondo (float): dimensión exterior Y (m).
        alto_piso (float): altura de entrepiso (libre + losa) en metros.
        grosor_muro (float): grosor de muros exteriores (m).
        grosor_losa (float): espesor de las losas (m).
        con_tejado (bool): añadir tejado a dos aguas sobre el último piso.
        altura_cumbrera (float): altura de la cumbrera del tejado (m).
        voladizo (float): voladizo del tejado sobre la fachada (m).
        origen (tuple): posición (x, y, z) de la esquina exterior inferior.
        material_muro (str): material de los muros.
        material_losa (str): material de las losas de entrepiso.
        material_tejado (str): material del tejado.

    Returns:
        bpy.types.Object: root (Empty) del activo casa.

    """
    root = _empty_root(nombre, "casa")
    root.location = Vector(origen)
    _set_meta(root, tipo="casa", pisos=pisos, ancho=ancho, fondo=fondo,
              alto_piso=alto_piso)

    alto_libre = alto_piso - grosor_losa  # altura libre interior por piso

    for p in range(pisos):
        z_base = p * alto_piso
        prefijo = f"{nombre}_P{p + 1}"

        # ── 4 muros exteriores ─────────────────────────────────────────
        g = grosor_muro
        # Sur  (a lo largo de X, Y=0)
        ms = crear_muro(f"{prefijo}_Muro_Sur",
                        largo=ancho, alto=alto_libre, grosor=g,
                        origen=(0, 0, z_base), material=material_muro)
        # Norte (a lo largo de X, Y=fondo−g)
        mn = crear_muro(f"{prefijo}_Muro_Norte",
                        largo=ancho, alto=alto_libre, grosor=g,
                        origen=(0, fondo - g, z_base), material=material_muro)
        # Oeste (a lo largo de Y, X=0)
        mo = crear_muro(f"{prefijo}_Muro_Oeste",
                        largo=fondo - 2*g, alto=alto_libre, grosor=g,
                        origen=(0, g, z_base), rotacion_z=90,
                        material=material_muro)
        # Este  (a lo largo de Y, X=ancho−g)
        me = crear_muro(f"{prefijo}_Muro_Este",
                        largo=fondo - 2*g, alto=alto_libre, grosor=g,
                        origen=(ancho - g, g, z_base), rotacion_z=90,
                        material=material_muro)

        for m in (ms, mn, mo, me):
            _parent(m, root)

        # ── Losa de techo / entrepiso ──────────────────────────────────
        losa = crear_losa_rectangular(f"{prefijo}_Losa",
                                      ancho=ancho, fondo=fondo,
                                      espesor=grosor_losa,
                                      origen=(0, 0, z_base + alto_libre),
                                      material=material_losa)
        _parent(losa, root)

    # ── Tejado a dos aguas sobre el último piso ────────────────────────
    if con_tejado:
        z_tejado = pisos * alto_piso
        tej = crear_tejado_dos_aguas(f"{nombre}_Tejado",
                                     ancho=ancho, fondo=fondo,
                                     altura_cumbrera=altura_cumbrera,
                                     espesor=0.12,
                                     voladizo_x=voladizo,
                                     voladizo_y=voladizo,
                                     origen=(0, 0, z_tejado),
                                     material=material_tejado)
        _parent(tej, root)

    return root


def crear_edificio_n_pisos(nombre="Edificio",
                            pisos=4,
                            ancho=12.0,
                            fondo=15.0,
                            alto_piso=2.80,
                            grosor_muro=0.20,
                            grosor_losa=0.20,
                            con_techo_plano=True,
                            con_columnas=False,
                            seccion_columna="rect",
                            dim_columna=0.30,
                            modulo_columna_x=4.0,
                            modulo_columna_y=5.0,
                            ventanas_fachada=True,
                            ventana_ancho=1.20,
                            ventana_alto=1.10,
                            ventana_alfeizar=0.90,
                            ventana_separacion=2.40,
                            origen=(0, 0, 0),
                            material_muro="Muro_Pintura",
                            material_losa="Hormigon",
                            material_fachada="Muro_Pintura_Gris",
                            material_vidrio="Vidrio_Templado",
                            material_marco="Marco_Aluminio",
                            material_columna="Hormigon"):
    """
    Genera un edificio de N pisos con planta rectangular: muros perimetrales,
    losas de entrepiso, techo plano opcional, rejilla de ventanas en fachada
    Sur/Norte y columnas estructurales opcionales.

    Args:
        nombre (str): nombre del activo raíz.
        pisos (int): número de plantas (≥ 1).
        ancho (float): dimensión exterior X (m).
        fondo (float): dimensión exterior Y (m).
        alto_piso (float): altura de entrepiso en metros.
        grosor_muro (float): grosor de muros exteriores (m).
        grosor_losa (float): espesor de losas (m).
        con_techo_plano (bool): añadir losa de cubierta plana.
        con_columnas (bool): generar columnas interiores en rejilla.
        seccion_columna (str): 'rect' o 'circ'.
        dim_columna (float): lado (rect) o diámetro (circ) de la columna (m).
        modulo_columna_x (float): separación entre columnas en X (m).
        modulo_columna_y (float): separación entre columnas en Y (m).
        ventanas_fachada (bool): abrir rejilla de ventanas en fachada Sur.
        ventana_ancho (float): ancho de cada ventana (m).
        ventana_alto (float): alto de cada ventana (m).
        ventana_alfeizar (float): altura del alféizar desde el suelo del piso (m).
        ventana_separacion (float): separación entre ventanas en X (m).
        origen (tuple): posición (x, y, z) de la esquina exterior inferior.
        material_muro (str): material de muros interiores.
        material_losa (str): material de losas.
        material_fachada (str): material de fachada exterior.
        material_vidrio (str): material del vidrio de ventanas.
        material_marco (str): material del marco de ventanas.
        material_columna (str): material de columnas.

    Returns:
        bpy.types.Object: root (Empty) del activo edificio.

    """
    root = _empty_root(nombre, "edificio")
    root.location = Vector(origen)
    _set_meta(root, tipo="edificio", pisos=pisos, ancho=ancho, fondo=fondo,
              alto_piso=alto_piso)

    alto_libre = alto_piso - grosor_losa
    g = grosor_muro

    for p in range(pisos):
        z_base = p * alto_piso
        prefijo = f"{nombre}_P{p + 1}"

        # ── Muros perimetrales ─────────────────────────────────────────
        ms = crear_muro(f"{prefijo}_Fachada_Sur",
                        largo=ancho, alto=alto_libre, grosor=g,
                        origen=(0, 0, z_base), material=material_fachada)
        mn = crear_muro(f"{prefijo}_Fachada_Norte",
                        largo=ancho, alto=alto_libre, grosor=g,
                        origen=(0, fondo - g, z_base), material=material_fachada)
        mo = crear_muro(f"{prefijo}_Fachada_Oeste",
                        largo=fondo - 2*g, alto=alto_libre, grosor=g,
                        origen=(0, g, z_base), rotacion_z=90,
                        material=material_fachada)
        me = crear_muro(f"{prefijo}_Fachada_Este",
                        largo=fondo - 2*g, alto=alto_libre, grosor=g,
                        origen=(ancho - g, g, z_base), rotacion_z=90,
                        material=material_fachada)

        for m in (ms, mn, mo, me):
            _parent(m, root)

        # ── Ventanas en fachada Sur (rejilla automática) ───────────────
        if ventanas_fachada:
            n_ventanas = max(1, int((ancho - ventana_separacion) //
                                    ventana_separacion))
            espacio_total = n_ventanas * ventana_ancho + (n_ventanas - 1) * (
                ventana_separacion - ventana_ancho)
            x_inicio = (ancho - espacio_total) / 2.0
            centros = []
            for k in range(n_ventanas):
                cx = x_inicio + k * ventana_separacion + ventana_ancho / 2.0
                cz = z_base + ventana_alfeizar + ventana_alto / 2.0
                centros.append((cx, 0.0, cz))
            abrir_vanos_batch_rectangulares(
                ms, centros_world=centros,
                ancho=ventana_ancho, alto=ventana_alto)
            for k, (cx, _, cz) in enumerate(centros):
                v = crear_ventana(f"{prefijo}_V_Sur_{k+1}",
                                  ancho=ventana_ancho, alto=ventana_alto,
                                  prof_marco=g,
                                  origen=(cx - ventana_ancho/2.0,
                                          0,
                                          cz - ventana_alto/2.0),
                                  material_vidrio=material_vidrio,
                                  material_marco=material_marco)
                _parent(v, root)

        # ── Losa de entrepiso ──────────────────────────────────────────
        losa = crear_losa_rectangular(f"{prefijo}_Losa",
                                      ancho=ancho, fondo=fondo,
                                      espesor=grosor_losa,
                                      origen=(0, 0, z_base + alto_libre),
                                      material=material_losa)
        _parent(losa, root)

        # ── Columnas interiores (rejilla) ──────────────────────────────
        if con_columnas:
            nx = max(1, int(ancho / modulo_columna_x) - 1)
            ny = max(1, int(fondo / modulo_columna_y) - 1)
            for ix in range(nx):
                for iy in range(ny):
                    cx = modulo_columna_x * (ix + 1)
                    cy = modulo_columna_y * (iy + 1)
                    col = crear_columna(
                        f"{prefijo}_Col_{ix}_{iy}",
                        seccion=seccion_columna,
                        ancho=dim_columna, fondo=dim_columna,
                        diametro=dim_columna,
                        alto=alto_libre,
                        origen=(cx, cy, z_base),
                        material=material_columna)
                    _parent(col, root)

    # ── Techo plano sobre el último piso ──────────────────────────────
    if con_techo_plano:
        z_techo = pisos * alto_piso
        techo = crear_techo_plano(f"{nombre}_Cubierta",
                                   ancho=ancho, fondo=fondo,
                                   espesor=grosor_losa,
                                   caida_x=0.02,
                                   origen=(0, 0, z_techo),
                                   material=material_losa)
        _parent(techo, root)

    return root


# ---------------------------------------------------------
#  GEOMETRÍA GENÉRICA
# ---------------------------------------------------------

def extruir_perfil(nombre="Extrusion",
                   puntos_2d=((0, 0), (2, 0), (2, 1), (0, 1)),
                   altura=3.0,
                   cerrar_perfil=True,
                   material="Generic"):
    """
    Extruye un perfil 2D plano (XY) hacia +Z.

    Args:
        nombre (str): nombre del activo.
        puntos_2d (list): lista de tuplas (x, y) que definen el contorno.
        altura (float): altura de extrusión en Z (m).
        cerrar_perfil (bool): si True, cierra el polígono.
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    bm = bmesh.new()
    verts = [bm.verts.new((x, y, 0)) for (x, y) in puntos_2d]
    bm.verts.ensure_lookup_table()
    face = bm.faces.new(verts if cerrar_perfil else verts[:-1])
    bm.faces.ensure_lookup_table()
    ex = bmesh.ops.extrude_face_region(bm, geom=[face])
    bmesh.ops.translate(
        bm, vec=(0, 0, altura),
        verts=[v for v in ex["geom"] if isinstance(v, bmesh.types.BMVert)],
    )
    mesh = bpy.data.meshes.new(nombre + "_mesh")
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(f"{nombre}_Solido", mesh)
    bpy.context.collection.objects.link(obj)
    asignar_material(obj, material)
    root = _empty_root(nombre, "extrusion")
    _parent(obj, root)
    _set_meta(root, tipo="extrusion", altura=altura,
              puntos=list(puntos_2d))
    return root


def extruir_con_huecos(nombre="Extr_Huecos",
                       contorno=((0, 0), (2, 0), (2, 1), (0, 1)),
                       agujeros=(),
                       altura=0.3,
                       material="Generic"):
    """
    Extruye un contorno 2D con agujeros internos usando operaciones booleanas.

    Args:
        nombre (str): nombre del activo.
        contorno (list): puntos 2D del contorno exterior.
        agujeros (list): lista de bucles — cada bucle es una lista de (x, y).
        altura (float): altura de extrusión (m).
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    outer_root = extruir_perfil(nombre=nombre, puntos_2d=tuple(contorno),
                                altura=altura, cerrar_perfil=True,
                                material=material)
    outer_mesh = _first_mesh_child(outer_root)

    cutters = []
    for i, hole in enumerate(agujeros, 1):
        cut_root = extruir_perfil(nombre=f"{nombre}_Hole{i}",
                                  puntos_2d=tuple(hole),
                                  altura=altura, cerrar_perfil=True,
                                  material=material)
        cutters.append(_first_mesh_child(cut_root))

    if cutters:
        if len(cutters) > 1:
            for o in bpy.context.view_layer.objects:
                o.select_set(False)
            bpy.context.view_layer.objects.active = cutters[0]
            for c in cutters:
                c.select_set(True)
            bpy.ops.object.join()
            cutter_union = bpy.context.active_object
        else:
            cutter_union = cutters[0]
        
        cutter_union.name = f"{nombre}_CutterUnion"
        _apply_boolean(outer_mesh, cutter_union)

    return outer_root


def crear_tuberia(nombre="Tuberia",
                  puntos_3d=((0, 0, 0), (0, 2, 0), (2, 2, 1)),
                  radio=0.05, resolucion=4,
                  origen=(0, 0, 0),
                  material="PVC"):
    """
    Crea una tubería/conducto a partir de una polilínea 3D.

    Args:
        nombre (str): nombre del activo.
        puntos_3d (list): lista de tuplas (x, y, z) que definen el eje.
        radio (float): radio exterior (m).
        resolucion (int): segmentos del círculo de sección.
        origen (tuple): posición (x, y, z) del root.
        material (str): nombre del material.

    Returns:
        bpy.types.Object: root (Empty) del activo.

    """
    curve_data = bpy.data.curves.new(nombre + "_path", type="CURVE")
    curve_data.dimensions = '3D'
    spl = curve_data.splines.new('POLY')
    spl.points.add(len(puntos_3d) - 1)
    for i, (x, y, z) in enumerate(puntos_3d):
        spl.points[i].co = (x, y, z, 1.0)
    curve_data.bevel_depth = radio
    curve_data.bevel_resolution = resolucion
    obj = bpy.data.objects.new(f"{nombre}_Curva", curve_data)
    obj.location = Vector(origen)
    bpy.context.collection.objects.link(obj)
    asignar_material(obj, material)
    root = _empty_root(nombre, "tuberia")
    root.location = Vector(origen)
    _parent(obj, root)
    _set_meta(root, tipo="tuberia", radio=radio,
              resolucion=resolucion, puntos=list(puntos_3d))
    return root


# ---------------------------------------------------------
#  ILUMINACIÓN Y CÁMARA
# ---------------------------------------------------------

def agregar_luz(nombre="Luz",
                tipo="POINT",
                ubicacion=(0, 0, 3),
                energia=1000.0,
                color=(1.0, 1.0, 1.0),
                radio=0.25,
                angulo_spot=45.0):
    """
    Añade una fuente de luz a la escena.

    Args:
        nombre (str): nombre del objeto luz.
        tipo (str): 'POINT', 'SUN', 'AREA', 'SPOT'.
        ubicacion (tuple): posición (x, y, z) en metros.
        energia (float): potencia en Watts (POINT/SPOT/AREA) o irradiancia (SUN).
        color (tuple): color RGB [0,1].
        radio (float): radio de la fuente (suaviza sombras) — para POINT/SPOT.
        angulo_spot (float): ángulo del cono en grados — solo para SPOT.

    Returns:
        bpy.types.Object: objeto luz.

    """
    luz_data = bpy.data.lights.new(nombre, type=tipo)
    luz_data.energy = energia
    luz_data.color  = color
    if hasattr(luz_data, 'shadow_soft_size'):
        luz_data.shadow_soft_size = radio
    if tipo == 'SPOT' and hasattr(luz_data, 'spot_size'):
        luz_data.spot_size = radians(angulo_spot)
    obj = bpy.data.objects.new(nombre, luz_data)
    obj.location = Vector(ubicacion)
    bpy.context.collection.objects.link(obj)
    return obj


def crear_camara(nombre="Camara",
                 ubicacion=(5, -7, 4),
                 rotacion=(60, 0, 45),
                 tipo="PERSP",
                 focal_length=35.0,
                 activa=True):
    """
    Añade una cámara a la escena y opcionalmente la establece como activa.

    Args:
        nombre (str): nombre de la cámara.
        ubicacion (tuple): posición (x, y, z) en metros.
        rotacion (tuple): rotación en grados (rx, ry, rz) — convenio XYZ Euler.
        tipo (str): 'PERSP' (perspectiva) o 'ORTHO' (ortogonal).
        focal_length (float): longitud focal en mm (solo PERSP).
        activa (bool): si True, establece como cámara activa de la escena.

    Returns:
        bpy.types.Object: objeto cámara.

    """
    cam_data = bpy.data.cameras.new(nombre)
    cam_data.type = tipo
    if tipo == 'PERSP':
        cam_data.lens = focal_length
    obj = bpy.data.objects.new(nombre, cam_data)
    obj.location = Vector(ubicacion)
    obj.rotation_euler = Euler(
        (radians(rotacion[0]), radians(rotacion[1]), radians(rotacion[2])),
        'XYZ',
    )
    bpy.context.collection.objects.link(obj)
    if activa:
        bpy.context.scene.camera = obj
    return obj


# ---------------------------------------------------------
#  UTILIDADES DE ESCENA
# ---------------------------------------------------------

def anclar_a(obj_mobile, obj_anchor,
             punto_anchor="centro",
             offset=(0, 0, 0)):
    """
    Reposiciona 'obj_mobile' relativo a 'obj_anchor'.

    Args:
        obj_mobile: objeto a mover (root o mesh).
        obj_anchor: objeto de referencia (root o mesh).
        punto_anchor (str): punto de referencia en obj_anchor:
            'centro', 'frente', 'detras', 'izquierda', 'derecha',
            'arriba', 'abajo', 'frente_izq', 'frente_der'.
        offset (tuple): desplazamiento adicional (dx, dy, dz) en metros.

    Returns:
        obj_mobile (con location actualizado).

    """
    # obtener bounding box world
    def _world_bb(obj):
        meshes = [obj] if obj.type == 'MESH' else [c for c in obj.children if c.type == 'MESH']
        if not meshes:
            corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
            xs, ys, zs = [c.x for c in corners], [c.y for c in corners], [c.z for c in corners]
            return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)
        
        xs, ys, zs = [], [], []
        for m in meshes:
            corners = [m.matrix_world @ Vector(c) for c in m.bound_box]
            xs.extend(c.x for c in corners)
            ys.extend(c.y for c in corners)
            zs.extend(c.z for c in corners)
        return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)

    xmn, xmx, ymn, ymx, zmn, zmx = _world_bb(obj_anchor)
    cx = (xmn + xmx) / 2.0
    cy = (ymn + ymx) / 2.0
    cz = (zmn + zmx) / 2.0

    puntos = {
        "centro":     (cx,  cy,  cz),
        "frente":     (cx,  ymn, cz),
        "detras":     (cx,  ymx, cz),
        "izquierda":  (xmn, cy,  cz),
        "derecha":    (xmx, cy,  cz),
        "arriba":     (cx,  cy,  zmx),
        "abajo":      (cx,  cy,  zmn),
        "frente_izq": (xmn, ymn, cz),
        "frente_der": (xmx, ymn, cz),
    }
    base = puntos.get(punto_anchor, (cx, cy, cz))
    obj_mobile.location = Vector((
        base[0] + offset[0],
        base[1] + offset[1],
        base[2] + offset[2],
    ))
    return obj_mobile


def limpiar_escena(mantener_colecciones=False):
    """
    Elimina todos los objetos de la escena activa (meshes, curvas, luces,
    cámaras, empties) y opcionalmente limpia colecciones.

    Args:
        mantener_colecciones (bool): si False, también elimina colecciones
            creadas por el usuario (excepto la Scene Collection).

    """
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.curves):
        if block.users == 0:
            bpy.data.curves.remove(block)
    for block in list(bpy.data.materials):
        if block.users == 0:
            bpy.data.materials.remove(block)
    if not mantener_colecciones:
        for col in list(bpy.data.collections):
            if col.users == 0:
                bpy.data.collections.remove(col)


def exportar_escena(ruta, formato="BLEND"):
    """
    Exporta la escena activa al formato especificado.

    Args:
        ruta (str): ruta absoluta del archivo de salida (con extensión).
        formato (str): 'BLEND', 'OBJ', 'FBX', 'GLTF', 'STL'.

    """
    fmt = formato.upper()
    if fmt == "BLEND":
        bpy.ops.wm.save_as_mainfile(filepath=ruta)
    elif fmt == "OBJ":
        bpy.ops.wm.obj_export(filepath=ruta, export_selected_objects=False)
    elif fmt == "FBX":
        bpy.ops.export_scene.fbx(filepath=ruta, use_selection=False)
    elif fmt in ("GLTF", "GLB"):
        bpy.ops.export_scene.gltf(filepath=ruta, export_format='GLB')
    elif fmt == "STL":
        bpy.ops.export_mesh.stl(filepath=ruta)
    else:
        raise ValueError(f"Formato no soportado: {formato}. "
                         f"Usa BLEND, OBJ, FBX, GLTF o STL.")
    print(f"[DSL] Escena exportada → {ruta}")



# ---------------------------------------------------------
#  VALIDACIÓN
# ---------------------------------------------------------

def validar_malla(obj_mesh, verbose=True):
    """
    Revisa una malla: aristas no-manifold, caras de área ~0 y aplica
    Mesh.validate() para correcciones automáticas.

    Args:
        obj_mesh: bpy.types.Object (MESH) o bpy.types.Mesh.
        verbose (bool): si True, imprime el reporte en consola.

    Returns:
        dict con claves:
            'non_manifold_edges' (int): aristas no-manifold.
            'zero_area_faces' (int): caras con área ≈ 0.
            'mesh_validate_fixed' (bool): True si validate() corrigió algo.
            'ok' (bool): True si la malla está limpia.

    """
    me = obj_mesh.data if hasattr(obj_mesh, "data") else obj_mesh
    bm = bmesh.new()
    bm.from_mesh(me)
    non_manifold = [e for e in bm.edges if not e.is_manifold]
    zero_area    = [f for f in bm.faces  if f.calc_area() <= 1e-12]
    bm.free()

    changed = me.validate(verbose=verbose)
    me.update()

    report = {
        "non_manifold_edges":  len(non_manifold),
        "zero_area_faces":     len(zero_area),
        "mesh_validate_fixed": bool(changed),
        "ok": len(non_manifold) == 0 and len(zero_area) == 0 and not changed,
    }
    if verbose:
        print("[DSL] VALIDACIÓN:", report)
    return report
