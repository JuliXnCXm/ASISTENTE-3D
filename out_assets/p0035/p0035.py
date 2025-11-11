import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_base = 0.40
altura_base = 0.05
altura_mastil = 1.60
diametro_mastil = 0.04
diametro_pantalla = 0.30

# Crear base
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_base / 2,
    depth=altura_base,
    location=(0, 0, altura_base / 2)
)
bpy.context.object.name = "BaseLampara"

# Crear mástil
altura_total_base = altura_base
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_mastil / 2,
    depth=altura_mastil,
    location=(0, 0, altura_total_base + altura_mastil / 2)
)
bpy.context.object.name = "MastilLampara"

# Crear pantalla (media esfera)
altura_total_mastil = altura_total_base + altura_mastil
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=diametro_pantalla / 2,
    location=(0, 0, altura_total_mastil)
)
pantalla = bpy.context.object
pantalla.name = "PantallaLampara"

# Cortar la esfera para hacer la pantalla (usando un booleano)
cortador = bpy.ops.mesh.primitive_cube_add(size=diametro_pantalla * 1.2, location=(0,0, altura_total_mastil - diametro_pantalla*0.6))
cortador_obj = bpy.context.object
cortador_obj.name = "CortadorBooleano"

bool_mod = pantalla.modifiers.new(name='Boolean', type='BOOLEAN')
bool_mod.object = cortador_obj
bool_mod.operation = 'DIFFERENCE'
bpy.ops.object.select_all(action='DESELECT')
pantalla.select_set(True)
bpy.context.view_layer.objects.active = pantalla
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

bpy.data.objects.remove(cortador_obj)