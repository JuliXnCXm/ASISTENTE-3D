import bpy
import bmesh

# Escena limpia y unidades en metros
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'
scene.unit_settings.scale_length = 1.0

# Parámetros
lado_largo = 3.0   # eje X
lado_corto = 2.0   # eje Y
fondo = 0.6        # profundidad de la encimera
espesor = 0.05     # grosor de la tapa
altura_suelo = 0.9 # altura de la cara superior

# Perfil 2D (L) en el plano XY con z=0 (n-gon cóncavo de 6 vértices)
verts = [
    (0.0,        0.0,        0.0),  # esquina interior
    (lado_largo, 0.0,        0.0),  # extremo lado largo
    (lado_largo, fondo,      0.0),  # exterior 1
    (fondo,      fondo,      0.0),  # codo interior de la 'L'
    (fondo,      lado_corto, 0.0),  # exterior 2
    (0.0,        lado_corto, 0.0)   # extremo lado corto
]

# Crear malla base y objeto
mesh = bpy.data.meshes.new('EncimeraProfileMesh')
mesh.from_pydata(verts, [], [(0, 1, 2, 3, 4, 5)])
mesh.update()
obj = bpy.data.objects.new('Encimera', mesh)
bpy.context.collection.objects.link(obj)

# Trabajar con BMesh para extruir volumen
bm = bmesh.new()
bm.from_mesh(mesh)
# Asegurar normales coherentes hacia +Z
bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
# Extruir región de la cara (devuelve mezcla de caras, aristas y vértices)
res = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
# Seleccionar SOLO vértices sin referir bmesh dentro de la list-comp (evita NameError)
verts_extruidos = [ele for ele in res['geom'] if hasattr(ele, 'co')]
# Trasladar en +Z el grosor
bmesh.ops.translate(bm, verts=verts_extruidos, vec=(0.0, 0.0, espesor))
# Escribir de vuelta
bm.to_mesh(mesh)
bm.free()
mesh.update()

# Colocar la encimera: cara superior a altura_suelo (superior en z=espesor)
obj.location.z = altura_suelo - espesor
