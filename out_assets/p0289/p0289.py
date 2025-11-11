import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros de la escalera
num_escalones = 5
contrahuella = 0.18 # Altura de cada escalón
radio_int = 0.5
radio_ext = 1.5
giro_total_grados = 90.0

giro_por_escalon_rad = math.radians(giro_total_grados / num_escalones)

# Crear el primer escalón como una malla
verts = []
# Vértices base (z=0)
verts.append((radio_int, 0, 0))
verts.append((radio_ext, 0, 0))
verts.append((radio_ext * math.cos(giro_por_escalon_rad), radio_ext * math.sin(giro_por_escalon_rad), 0))
verts.append((radio_int * math.cos(giro_por_escalon_rad), radio_int * math.sin(giro_por_escalon_rad), 0))
# Vértices superiores (z=contrahuella)
for i in range(4):
    v = verts[i]
    verts.append((v[0], v[1], contrahuella))

faces = [
    (0, 1, 2, 3), # Base
    (4, 5, 6, 7), # Tapa
    (0, 1, 5, 4), # Cara frontal
    (2, 3, 7, 6), # Cara trasera
    (1, 2, 6, 5), # Cara exterior
    (0, 3, 7, 4)  # Cara interior
]

mesh_escalon = bpy.data.meshes.new('MeshEscalonBase')
mesh_escalon.from_pydata(verts, [], faces)
obj_escalon_base = bpy.data.objects.new('EscalonBase', mesh_escalon)
bpy.context.collection.objects.link(obj_escalon_base)

# Crear los escalones usando un array modifier
bpy.context.view_layer.objects.active = obj_escalon_base

# Crear un empty para el giro
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
empty_pivote = bpy.context.active_object

# Seleccionar el escalón base de nuevo
bpy.context.view_layer.objects.active = obj_escalon_base

array_mod = obj_escalon_base.modifiers.new(name='ArrayEscalera', type='ARRAY')
array_mod.count = num_escalones
array_mod.use_relative_offset = False
array_mod.use_object_offset = True
array_mod.offset_object = empty_pivote

# Configurar la transformación del empty
empty_pivote.location.z = contrahuella
empty_pivote.rotation_euler.z = giro_por_escalon_rad

obj_escalon_base.name = 'EscaleraCaracol'