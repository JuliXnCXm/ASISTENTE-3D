import bpy
import bmesh

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Parámetros de la escalera
num_peldaños = 12
huella = 0.30
contrahuella = 0.18
ancho = 1.2
espesor_losa = 0.15

# Crear vértices del perfil lateral
verts = [(0, 0, 0)]
for i in range(num_peldaños):
    x_act = i * huella
    z_act = i * contrahuella
    verts.append((x_act, 0, z_act + contrahuella))
    verts.append((x_act + huella, 0, z_act + contrahuella))

# Vértices inferiores de la losa
ultimo_punto = verts[-1]
primer_punto = verts[0]
import math
angulo = math.atan2(ultimo_punto[2] - primer_punto[2], ultimo_punto[0] - primer_punto[0])
dx = espesor_losa * math.sin(angulo)
dz = espesor_losa * math.cos(angulo)

verts.append((ultimo_punto[0] - dx, 0, ultimo_punto[2] - dz))
verts.append((primer_punto[0] - dx, 0, primer_punto[2] - dz))

# Crear malla y objeto
mesh = bpy.data.meshes.new(name='PerfilEscalera')
obj = bpy.data.objects.new('EscaleraHormigon', mesh)
scene.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bm = bmesh.new()
bm.from_mesh(mesh)

for v_co in verts:
    bm.verts.new(v_co)

bm.faces.new(bm.verts)

bm.to_mesh(mesh)
bm.free()

# Extruir el perfil para darle ancho
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={'value':(0, ancho, 0)})
bpy.ops.object.mode_set(mode='OBJECT')