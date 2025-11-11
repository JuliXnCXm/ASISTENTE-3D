import bpy
import bmesh
import math

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros
altura = 1.5
espesor = 0.3
radio_interior = 5.0
angulo_total = 90.0 # Grados
segmentos = 32

# --- Crear malla y bmesh
malla = bpy.data.meshes.new("MuroCurvo")
bm = bmesh.new()

radio_exterior = radio_interior + espesor
angulo_rad = math.radians(angulo_total)

verts_abajo_int = []
verts_abajo_ext = []

# --- Generar vértices de la base
for i in range(segmentos + 1):
    angulo = (i / segmentos) * angulo_rad
    x_int = radio_interior * math.cos(angulo)
    y_int = radio_interior * math.sin(angulo)
    x_ext = radio_exterior * math.cos(angulo)
    y_ext = radio_exterior * math.sin(angulo)
    
    verts_abajo_int.append(bm.verts.new((x_int, y_int, 0)))
    verts_abajo_ext.append(bm.verts.new((x_ext, y_ext, 0)))

# --- Extruir hacia arriba para crear los muros
geom_superior = bmesh.ops.extrude_edge_only(bm, edges=bm.edges[:])
verts_superiores = [v for v in geom_superior['geom'] if isinstance(v, bmesh.types.BMVert)]
bmesh.ops.translate(bm, verts=verts_superiores, vec=(0, 0, altura))

# --- Crear tapas
bmesh.ops.contextual_create(bm, geom=bm.verts[:] + bm.edges[:])

# --- Finalizar
bm.to_mesh(malla)
bm.free()

objeto_muro = bpy.data.objects.new("MuroCurvoContencion", malla)
scene.collection.objects.link(objeto_muro)