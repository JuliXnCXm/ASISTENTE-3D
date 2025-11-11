# blender_arch.py
# ============================================================
# Librería atómica y paramétrica para arquitectura en Blender
# Requiere: ejecutar dentro de Blender (bpy, bmesh)
# Unidades: metros. Ejes: X=ancho, Y=fondo/profundidad, Z=alto
# Cada función crea un activo autocontenido con un root (Empty) y metadatos.
# ============================================================
import bpy
import bmesh
import json
from math import atan2, radians, tan
from mathutils import Vector, Matrix

# --------------------------- Helpers base ---------------------------

def _first_mesh_child(root_or_obj):
    """Devuelve el primer hijo MESH si pasas un root (Empty). Si pasas un MESH, lo devuelve tal cual."""
    if isinstance(root_or_obj, bpy.types.Object) and root_or_obj.type == 'MESH':
        return root_or_obj
    if isinstance(root_or_obj, bpy.types.Object) and root_or_obj.type == 'EMPTY':
        for ch in root_or_obj.children:
            if ch.type == 'MESH':
                return ch
    raise ValueError("No se encontró objeto MESH válido (pasa el root del activo o el MESH directo).")

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
    # Caja con origen en la esquina mínima (0,0,0) y dimensiones +X,+Y,+Z
    verts = [
        (0,0,0),(sx,0,0),(sx,sy,0),(0,sy,0),
        (0,0,sz),(sx,0,sz),(sx,sy,sz),(0,sy,sz)
    ]
    faces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),
             (1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return _new_mesh_object(name, verts, faces)

def _empty_root(nombre, categoria):
    root = bpy.data.objects.new(nombre, None)
    root.empty_display_type = 'ARROWS'
    root["arch_categoria"] = categoria
    bpy.context.collection.objects.link(root)
    return root

def _set_meta(root, **params):
    # Guarda parámetros como propiedades ID (planas) y como JSON
    root["arch_params_json"] = json.dumps(params)
    for k, v in params.items():
        try:
            root[f"arch_{k}"] = float(v) if isinstance(v, (int, float)) else str(v)
        except Exception:
            root[f"arch_{k}"] = str(v)

def _parent(child, parent):
    child.parent = parent
    # Mantener transforms locales (no aplicar)
    child.matrix_parent_inverse = parent.matrix_world.inverted()

def asignar_material(obj, nombre="Mat",
                     base_color=(0.8,0.8,0.8,1.0),
                     roughness=0.5, metallic=0.0, transmission=0.0, ior=1.45):
    """
    Crea o reutiliza un Principled BSDF y lo asigna.
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
        # Transparencia tipo vidrio
        if "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        if "IOR" in bsdf.inputs:
            bsdf.inputs["IOR"].default_value = ior
    # asignar
    if obj.data and hasattr(obj.data, "materials"):
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
    return mat

# --------------------------- Primitivas atómicas ---------------------------

def crear_muro(nombre="Muro",
               largo=4.0, alto=3.0, grosor=0.2,
               origen=(0,0,0),
               material="Muro_Generic"):
    """
    Crea un muro rectangular (prisma) alineado a +X (largo), +Y (grosor), +Z (alto).
    Args:
        largo (m), alto (m), grosor (m)
    """
    root = _empty_root(nombre, "muro")
    muro = _box(f"{nombre}_Cuerpo", largo, grosor, alto)
    muro.location = Vector(origen)
    asignar_material(muro, material)
    _parent(muro, root)
    _set_meta(root, tipo="muro", largo=largo, alto=alto, grosor=grosor, origen=origen)
    return root

def crear_ventana(nombre="Ventana",
                  ancho=1.2, alto=1.2,
                  espesor_marco=0.06, prof_marco=0.08,
                  divisiones=(1,1), espesor_divisor=0.03,
                  espesor_vidrio=0.006, retranqueo_vidrio=0.02,
                  material_marco="Marco_Pintura", material_vidrio="Vidrio"):
    """
    Crea una ventana paramétrica (marco + divisiones + vidrios).
    Origen en esquina inferior-trasera (0,0,0). Extiende +X (ancho), +Y (prof), +Z (alto).
    Args:
        divisiones: (nx, ny) -> columnas x filas de paños (>=1). Se crean divisores (nx-1) y (ny-1).
    """
    nx, ny = max(1, int(divisiones[0])), max(1, int(divisiones[1]))
    clear_w = max(0.01, ancho - 2*espesor_marco)
    clear_h = max(0.01, alto  - 2*espesor_marco)
    root = _empty_root(nombre, "ventana")
    _set_meta(root, tipo="ventana", ancho=ancho, alto=alto, espesor_marco=espesor_marco,
              prof_marco=prof_marco, nx=nx, ny=ny, espesor_divisor=espesor_divisor,
              espesor_vidrio=espesor_vidrio, retranqueo_vidrio=retranqueo_vidrio)
    j_izq = _box(f"{nombre}_Jamba_Izq", espesor_marco, prof_marco, alto)
    j_der = _box(f"{nombre}_Jamba_Der", espesor_marco, prof_marco, alto); j_der.location.x = ancho - espesor_marco
    t_inf = _box(f"{nombre}_Travesanio_Inf", ancho - 2*espesor_marco, prof_marco, espesor_marco)
    t_inf.location = Vector((espesor_marco, 0, 0))
    t_sup = _box(f"{nombre}_Travesanio_Sup", ancho - 2*espesor_marco, prof_marco, espesor_marco)
    t_sup.location = Vector((espesor_marco, 0, alto - espesor_marco))

    for p in (j_izq, j_der, t_inf, t_sup):
        asignar_material(p, material_marco); _parent(p, root)

    if nx > 1:
        paso = clear_w / nx
        for i in range(1, nx):
            x = espesor_marco + i*paso - espesor_divisor/2.0
            mull = _box(f"{nombre}_Mul_V_{i}", espesor_divisor, prof_marco, clear_h)
            mull.location = Vector((x, 0, espesor_marco))
            asignar_material(mull, material_marco); _parent(mull, root)
    if ny > 1:
        paso = clear_h / ny
        for j in range(1, ny):
            z = espesor_marco + j*paso - espesor_divisor/2.0
            mull = _box(f"{nombre}_Mul_H_{j}", clear_w, prof_marco, espesor_divisor)
            mull.location = Vector((espesor_marco, 0, z))
            asignar_material(mull, material_marco); _parent(mull, root)

    # Vidrios (paneles)
    vidrio_mat = asignar_material(_box(f"{nombre}_Vidrio_TMP", 0.01, 0.01, 0.01), material_vidrio,
                                  base_color=(0.7,0.85,1.0,1.0), roughness=0.05, metallic=0.0, transmission=1.0, ior=1.45)
    bpy.data.objects.remove(bpy.data.objects[f"{nombre}_Vidrio_TMP"], do_unlink=True)

    pane_w = (clear_w - (nx-1)*espesor_divisor) / nx
    pane_h = (clear_h - (ny-1)*espesor_divisor) / ny
    for ix in range(nx):
        for iy in range(ny):
            x = espesor_marco + ix*(pane_w + espesor_divisor)
            z = espesor_marco + iy*(pane_h + espesor_divisor)
            panel = _box(f"{nombre}_Vidrio_{ix+1}_{iy+1}", pane_w, max(0.002, prof_marco - retranqueo_vidrio), pane_h)
            panel.location = Vector((x, retranqueo_vidrio, z))
            panel.data.materials.append(vidrio_mat)
            _parent(panel, root)

    return root

def crear_puerta(nombre="Puerta",
                 ancho=0.9, alto=2.1,
                 espesor_panel=0.04,
                 ancho_marco=0.08, prof_marco=0.1,
                 holgura=0.005,
                 material_panel="Madera", material_marco="Marco_Pintura"):
    """
    Crea una puerta batiente simple (panel + marco U).
    Origen en esquina inferior-trasera del marco.
    """
    root = _empty_root(nombre, "puerta")
    _set_meta(root, tipo="puerta", ancho=ancho, alto=alto, espesor_panel=espesor_panel,
              ancho_marco=ancho_marco, prof_marco=prof_marco, holgura=holgura)

    # Marco: jambas + dintel
    j_izq = _box(f"{nombre}_Jamba_Izq", ancho_marco, prof_marco, alto)
    j_der = _box(f"{nombre}_Jamba_Der", ancho_marco, prof_marco, alto); j_der.location.x = ancho - ancho_marco
    dintel = _box(f"{nombre}_Dintel", ancho - 2*ancho_marco, prof_marco, ancho_marco)
    dintel.location = Vector((ancho_marco, 0, alto - ancho_marco))
    for p in (j_izq, j_der, dintel):
        asignar_material(p, material_marco); _parent(p, root)

    # Hoja/panel
    clear_w = ancho - 2*ancho_marco - 2*holgura
    clear_h = alto - ancho_marco - 2*holgura
    panel = _box(f"{nombre}_Panel", clear_w, espesor_panel, clear_h)
    panel.location = Vector((ancho_marco + holgura, (prof_marco - espesor_panel)/2.0, holgura))
    asignar_material(panel, material_panel); _parent(panel, root)
    return root

def crear_techo_plano(nombre="TechoPlano",
                      ancho=6.0, fondo=4.0, espesor=0.20,
                      caida_x=0.0, caida_y=0.0,
                      origen=(0,0,3.0),
                      material="Losacero/Placa"):
    """
    Crea una LOSA/PLACA rectangular con pendiente simple.
    - caida_x: ΔZ (m) desde X=0 a X=ancho (positivo baja hacia +X).
    - caida_y: ΔZ (m) desde Y=0 a Y=fondo.
    Origen = esquina inferior baja (en (0,0,Z0)).
    """
    # vértices base (inferior)
    z0 = origen[2]
    v0 = (0,      0,      z0)
    v1 = (ancho,  0,      z0)
    v2 = (ancho,  fondo,  z0)
    v3 = (0,      fondo,  z0)

    # vértices superiores (aplican caídas)
    z10 = z0 + espesor - caida_x
    z11 = z0 + espesor - caida_x - caida_y
    z01 = z0 + espesor - caida_y
    v4 = (0,      0,      z0+espesor)
    v5 = (ancho,  0,      z10)
    v6 = (ancho,  fondo,  z11)
    v7 = (0,      fondo,  z01)

    verts = [v0,v1,v2,v3,v4,v5,v6,v7]
    faces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    placa = _new_mesh_object(f"{nombre}_Cuerpo", verts, faces)
    placa.location = Vector((origen[0], origen[1], 0))
    asignar_material(placa, material)
    root = _empty_root(nombre, "techo_plano")
    _parent(placa, root)
    _set_meta(root, tipo="techo_plano", ancho=ancho, fondo=fondo, espesor=espesor,
              caida_x=caida_x, caida_y=caida_y, origen=origen)
    return root

def crear_silla(nombre="Silla",
                ancho=0.45, fondo=0.45,
                alto_asiento=0.45, alto_respaldo=0.9,
                grosor=0.03,
                material="Madera"):
    """
    Silla cúbica simple (4 patas + asiento + respaldo).
    """
    root = _empty_root(nombre, "silla")
    _set_meta(root, tipo="silla", ancho=ancho, fondo=fondo, alto_asiento=alto_asiento,
              alto_respaldo=alto_respaldo, grosor=grosor)
    # patas
    for dx in (0, ancho-grosor):
        for dy in (0, fondo-grosor):
            pata = _box(f"{nombre}_Pata", grosor, grosor, alto_asiento)
            pata.location = Vector((dx, dy, 0))
            asignar_material(pata, material); _parent(pata, root)
    # asiento
    asiento = _box(f"{nombre}_Asiento", ancho, fondo, grosor)
    asiento.location = Vector((0, 0, alto_asiento))
    asignar_material(asiento, material); _parent(asiento, root)
    # respaldo
    respaldo = _box(f"{nombre}_Respaldo", grosor, fondo, max(0.0, alto_respaldo - alto_asiento))
    respaldo.location = Vector((0, 0, alto_asiento))
    asignar_material(respaldo, material); _parent(respaldo, root)
    return root

def crear_sofa(nombre="Sofa",
               ancho=2.0, fondo=0.9, alto_asiento=0.45,
               alto_respaldo=0.85, ancho_brazo=0.12, grosor=0.1,
               material="Tela", material_estructura="Madera"):
    """
    Sofá de 2-3 plazas simple (base + cojín + respaldo + brazos).
    """
    root = _empty_root(nombre, "sofa")
    _set_meta(root, tipo="sofa", ancho=ancho, fondo=fondo, alto_asiento=alto_asiento,
              alto_respaldo=alto_respaldo, ancho_brazo=ancho_brazo, grosor=grosor)
    # base
    base = _box(f"{nombre}_Base", ancho, fondo, grosor)
    asignar_material(base, material_estructura); _parent(base, root)
    # cojín asiento
    coj = _box(f"{nombre}_Cojin", ancho-2*0.04, fondo-2*0.04, 0.12)
    coj.location = Vector((0.02, 0.02, grosor))
    asignar_material(coj, material); _parent(coj, root)
    # respaldo
    res = _box(f"{nombre}_Respaldo", ancho-2*ancho_brazo, grosor, alto_respaldo - alto_asiento)
    res.location = Vector((ancho_brazo, fondo - grosor, alto_asiento))
    asignar_material(res, material); _parent(res, root)
    # brazos
    b1 = _box(f"{nombre}_Brazo_Izq", ancho_brazo, fondo, alto_respaldo)
    b2 = _box(f"{nombre}_Brazo_Der", ancho_brazo, fondo, alto_respaldo); b2.location.x = ancho - ancho_brazo
    for b in (b1,b2):
        asignar_material(b, material_estructura); _parent(b, root)
    return root

def crear_cama(nombre="Cama",
               ancho=1.6, largo=2.0, alto_base=0.35, alto_cabecero=1.0,
               grosor_base=0.06, grosor_colchon=0.25,
               material_base="Madera", material_colchon="Textil"):
    """
    Cama con base, colchón y cabecero.
    Origen en esquina inferior-trasera de la base.
    """
    root = _empty_root(nombre, "cama")
    _set_meta(root, tipo="cama", ancho=ancho, largo=largo, alto_base=alto_base,
              alto_cabecero=alto_cabecero, grosor_base=grosor_base, grosor_colchon=grosor_colchon)
    base = _box(f"{nombre}_Base", ancho, largo, grosor_base)
    asignar_material(base, material_base); _parent(base, root)
    colchon = _box(f"{nombre}_Colchon", ancho-0.04, largo-0.04, grosor_colchon)
    colchon.location = Vector((0.02, 0.02, grosor_base))
    asignar_material(colchon, material_colchon); _parent(colchon, root)
    cab = _box(f"{nombre}_Cabecero", ancho, 0.06, alto_cabecero)
    cab.location = Vector((0, 0, alto_base))
    asignar_material(cab, material_base); _parent(cab, root)
    return root

def crear_tuberia(nombre="Tuberia",
                  puntos_3d=((0,0,0),(0,2,0),(2,2,1)),
                  radio=0.05, resolucion=2, material="PVC"):
    """
    Tubería a partir de polilínea 3D usando curva con 'bevel'.
    """
    curve_data = bpy.data.curves.new(nombre + "_path", type="CURVE")
    curve_data.dimensions = '3D'
    spl = curve_data.splines.new('POLY')
    spl.points.add(len(puntos_3d)-1)
    for i, (x,y,z) in enumerate(puntos_3d):
        spl.points[i].co = (x, y, z, 1.0)
    curve_data.bevel_depth = radio
    curve_data.bevel_resolution = resolucion
    obj = bpy.data.objects.new(f"{nombre}_Curva", curve_data)
    bpy.context.collection.objects.link(obj)
    asignar_material(obj, material)
    root = _empty_root(nombre, "tuberia")
    _parent(obj, root)
    _set_meta(root, tipo="tuberia", radio=radio, resolucion=resolucion, puntos=list(puntos_3d))
    return root

def extruir_perfil(nombre="Extrusion",
                   puntos_2d=((0,0),(2,0),(2,1),(0,1)),
                   altura=3.0,
                   cerrar_perfil=True,
                   material="Generic"):
    """
    Extruye un perfil plano (XY) hacia +Z.
    """
    bm = bmesh.new()
    verts = [bm.verts.new((x,y,0)) for (x,y) in puntos_2d]
    bm.verts.ensure_lookup_table()
    if cerrar_perfil:
        face = bm.faces.new(verts)
    else:
        face = bm.faces.new(verts[:-1])
    bm.faces.ensure_lookup_table()
    geom_ex = bmesh.ops.extrude_face_region(bm, geom=[face])
    bmesh.ops.translate(bm, vec=(0,0,altura),
                        verts=[v for v in geom_ex["geom"] if isinstance(v, bmesh.types.BMVert)])
    mesh = bpy.data.meshes.new(nombre + "_mesh")
    bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(f"{nombre}_Solido", mesh)
    bpy.context.collection.objects.link(obj)
    asignar_material(obj, material)
    root = _empty_root(nombre, "extrusion")
    _parent(obj, root)
    _set_meta(root, tipo="extrusion", altura=altura, puntos=list(puntos_2d))
    return root

def abrir_vanos_batch_rectangulares(muro, centros_world,
                                    ancho=1.2, alto=1.2, profundidad=None,
                                    aplicar=True, nombre="VanosBatch"):
    """
    Abre múltiples huecos rectangulares en un muro con UNA sola operación booleana.
    - 'muro' puede ser root o el MESH del muro.
    - 'centros_world': lista de (x,y,z) en coordenadas globales (centro del vano).
    """
    muro_mesh = _first_mesh_child(muro)
    # grosor local del muro
    ys = [v[1] for v in muro_mesh.bound_box]
    grosor_local = (max(ys) - min(ys)) if ys else 0.2
    prof = profundidad if profundidad else grosor_local * 1.05

    # crear todos los cutters orientados al eje local del muro
    cutters = []
    M = muro_mesh.matrix_world
    Minv = M.inverted()
    for i, c in enumerate(centros_world, 1):
        pos_local = Minv @ Vector(c)
        # Caja con origen en esquina mínima → centramos con offset
        cutter = _box(f"{nombre}_cutter_{i}", ancho, prof, alto)
        local_offset = Matrix.Translation(pos_local - Vector((ancho/2.0, prof/2.0, alto/2.0)))
        cutter.matrix_world = M @ local_offset
        cutters.append(cutter)

    if not cutters:
        return muro_mesh

    for o in bpy.context.view_layer.objects: o.select_set(False)
    active = cutters[0]
    bpy.context.view_layer.objects.active = active
    for c in cutters: c.select_set(True)
    bpy.ops.object.join()
    cutter_union = active
    cutter_union.name = f"{nombre}_Union"
    bool_mod = muro_mesh.modifiers.new(f"{nombre}_Bool", 'BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.solver = 'EXACT'
    bool_mod.object = cutter_union
    bpy.context.view_layer.objects.active = muro_mesh
    if aplicar:
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)
        bpy.data.objects.remove(cutter_union, do_unlink=True)
    return muro_mesh

def abrir_vanos_grid_local(muro, filas=3, cols=4,
                           x0=1.2, z0=1.2, dx=1.8, dz=3.0,
                           ancho=1.2, alto=1.2, profundidad=None,
                           nombre="VanosGrid", aplicar=True):
    """
    Genera una rejilla (filas x columnas) de vanos EN EL SISTEMA LOCAL DEL MURO.
    x0,z0: centro del primer vano en local (Y se calcula al centro del grosor).
    dx,dz: separación entre centros en local.
    """
    muro_mesh = _first_mesh_child(muro)
    # centro Y local
    ys = [v[1] for v in muro_mesh.bound_box]
    grosor_local = (max(ys) - min(ys)) if ys else 0.2
    yctr = (min(ys) + max(ys))/2.0

    M = muro_mesh.matrix_world
    centros_world = []
    for r in range(filas):
        for c in range(cols):
            p_local = Vector((x0 + c*dx, yctr, z0 + r*dz))
            centros_world.append(tuple(M @ p_local))
    return abrir_vanos_batch_rectangulares(muro_mesh, centros_world, ancho, alto, profundidad, aplicar, nombre)

def extruir_con_huecos(nombre="Extr_Huecos",
                       contorno=((0,0),(2,0),(2,1),(0,1)),
                       agujeros=(),  # lista de bucles: [ [(x,y),...], [(x,y),...] ]
                       altura=0.3,
                       material="Generic"):
    """
    Crea una extrusión 3D a partir de un contorno con 'n' agujeros internos.
    Implementación: extruye el contorno exterior y Resta (Boolean) las extrusiones de cada agujero.
    """
    # 1) sólido exterior
    outer_root = extruir_perfil(nombre=nombre, puntos_2d=tuple(contorno), altura=altura, cerrar_perfil=True, material=material)
    outer_mesh = _first_mesh_child(outer_root)

    # 2) cutters para agujeros
    cutters = []
    for i, hole in enumerate(agujeros, 1):
        cut_root = extruir_perfil(nombre=f"{nombre}_Hole{i}", puntos_2d=tuple(hole), altura=altura, cerrar_perfil=True, material=material)
        cut_mesh = _first_mesh_child(cut_root)
        cutters.append(cut_mesh)

    if cutters:
        # unir cutters en un solo objeto para 1 boolean (más rápido)
        for o in bpy.context.view_layer.objects: o.select_set(False)
        active = cutters[0]
        bpy.context.view_layer.objects.active = active
        for c in cutters:
            c.select_set(True)
        bpy.ops.object.join()
        cutter_union = active
        cutter_union.name = f"{nombre}_CutterUnion"

        # Boolean difference
        bool_mod = outer_mesh.modifiers.new(f"{nombre}_Bool", 'BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.solver = 'EXACT'
        bool_mod.object = cutter_union
        bpy.context.view_layer.objects.active = outer_mesh
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)

        # limpiar cutters
        bpy.data.objects.remove(cutter_union, do_unlink=True)

    return outer_root

def crear_columna(nombre="Columna",
                  seccion="rect",  # 'rect' o 'circ'
                  ancho=0.30, fondo=0.30, diametro=0.30,
                  alto=3.0, material="Hormigon"):
    """
    Crea una columna paramétrica:
    - seccion='rect': usa ancho (X) y fondo (Y)
    - seccion='circ': usa diametro
    """
    root = _empty_root(nombre, "columna")
    if seccion.lower().startswith('c'):  # circular
        # cilindro vía bmesh
        bm = bmesh.new()
        bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=32,
            radius1=diametro/2.0,
            radius2=diametro/2.0,
            depth=alto
        )
        me = bpy.data.meshes.new(f"{nombre}_mesh")
        bm.to_mesh(me); bm.free()
        obj = bpy.data.objects.new(f"{nombre}_Cuerpo", me)
        bpy.context.collection.objects.link(obj)
    else:
        obj = _box(f"{nombre}_Cuerpo", ancho, fondo, alto)
    asignar_material(obj, material)
    _parent(obj, root)
    _set_meta(root, tipo="columna", seccion=seccion, ancho=ancho, fondo=fondo, diametro=diametro, alto=alto)
    return root

def crear_losa_rectangular(nombre="Losa",
                           ancho=4.0, fondo=3.0, espesor=0.20, material="Hormigon"):
    """
    Crea una losa rectangular (ancho X, fondo Y, espesor Z).
    """
    pts = ((0,0),(ancho,0),(ancho,fondo),(0,fondo))
    return extruir_perfil(nombre=nombre, puntos_2d=pts, altura=espesor, cerrar_perfil=True, material=material)

def crear_escalera_recta(nombre="Escalera",
                         huella=0.28, contrahuella=0.175, ancho=1.1,
                         num_peldanos=16, grosor=0.05, material="Hormigon"):
    """
    Crea una escalera recta (peldaños como prismas). Origen en la esquina de la primera huella.
    """
    root = _empty_root(nombre, "escalera_recta")
    _set_meta(root, tipo="escalera_recta", huella=huella, contrahuella=contrahuella, ancho=ancho, num=num_peldanos, grosor=grosor)
    for i in range(num_peldanos):
        paso = _box(f"{nombre}_Peldaño_{i+1}", huella, ancho, grosor)
        paso.location = Vector((i*huella, 0, i*contrahuella))
        asignar_material(paso, material)
        _parent(paso, root)
    return root

def crear_mesa(nombre="Mesa",
               ancho=1.6, fondo=0.8, alto=0.75,
               grosor_tablero=0.04, espesor_pata=0.05,
               setback_pata=0.06,
               material_tablero="Madera", material_patas="Metal"):
    """
    Mesa rectangular con 4 patas.
    """
    root = _empty_root(nombre, "mesa")
    _set_meta(root, tipo="mesa", ancho=ancho, fondo=fondo, alto=alto,
              grosor_tablero=grosor_tablero, espesor_pata=espesor_pata, setback_pata=setback_pata)

    tablero = _box(f"{nombre}_Tablero", ancho, fondo, grosor_tablero)
    tablero.location = Vector((0,0,alto - grosor_tablero))
    asignar_material(tablero, material_tablero); _parent(tablero, root)

    for dx in (setback_pata, ancho - setback_pata - espesor_pata):
        for dy in (setback_pata, fondo - setback_pata - espesor_pata):
            pata = _box(f"{nombre}_Pata", espesor_pata, espesor_pata, alto - grosor_tablero)
            pata.location = Vector((dx, dy, 0))
            asignar_material(pata, material_patas); _parent(pata, root)
    return root

def validar_malla(obj_mesh, verbose=True):
    """
    Revisa una malla: aristas no-manifold, caras de área ~0, y usa Mesh.validate().
    Devuelve un dict con el reporte.
    """
    me = obj_mesh.data if hasattr(obj_mesh, "data") else obj_mesh
    # BMesh para chequeos
    bm = bmesh.new(); bm.from_mesh(me)
    non_manifold = [e for e in bm.edges if not e.is_manifold]
    zero_area = [f for f in bm.faces if f.calc_area() <= 1e-12]
    bm.free()

    changed = me.validate(verbose=verbose)  # True si realizó correcciones
    me.update()

    report = {
        "non_manifold_edges": len(non_manifold),
        "zero_area_faces": len(zero_area),
        "mesh_validate_fixed": bool(changed),
    }
    if verbose:
        print("VALIDACIÓN:", report)
    return report

def compilar_archivo_py(ruta):
    import py_compile
    try:
        py_compile.compile(ruta, doraise=True)
        print("OK: compilación de", ruta)
        return True
    except py_compile.PyCompileError as e:
        print("ERROR de compilación:", e.msg)
        return False

def crear_baranda_lineal(nombre="Baranda",
                         largo=4.0, altura=1.0,
                         poste_cada=1.2, seccion_poste=0.04,
                         seccion_pasamanos=(0.04, 0.08),
                         material="Metal"):
    """
    Baranda lineal a lo largo de X, con postes cada 'poste_cada' y 2 pasamanos (superior e intermedio).
    """
    root = _empty_root(nombre, "baranda")
    _set_meta(root, tipo="baranda", largo=largo, altura=altura, poste_cada=poste_cada)

    # postes
    n_postes = max(2, int(largo / poste_cada) + 1)
    step = largo / (n_postes - 1)
    for i in range(n_postes):
        x = i*step
        post = _box(f"{nombre}_Poste_{i+1}", seccion_poste, seccion_poste, altura)
        post.location = Vector((x, 0, 0))
        asignar_material(post, material); _parent(post, root)

    # pasamanos: (ancho=X, fondo=Y)
    pw, py = seccion_pasamanos
    top = _box(f"{nombre}_PasamanosTop", largo, py, pw)
    top.location = Vector((0, 0, altura - pw))
    mid = _box(f"{nombre}_PasamanosMid", largo, py, pw)
    mid.location = Vector((0, 0, altura*0.5))
    for rail in (top, mid):
        asignar_material(rail, material); _parent(rail, root)
    return root
