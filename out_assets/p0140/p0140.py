import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_base = 0.30
altura_base = 0.02
altura_mastil = 1.5
diametro_mastil = 0.03
diametro_pantalla = 0.40

# Base
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_base / 2,
    depth=altura_base,
    location=(0, 0, altura_base / 2)
)
bpy.context.active_object.name = "BaseLampara"

# Mástil
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_mastil / 2,
    depth=altura_mastil,
    location=(0, 0, altura_base + altura_mastil / 2)
)
bpy.context.active_object.name = "MastilLampara"

# Pantalla semiesférica por booleano
altura_total = altura_base + altura_mastil
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=diametro_pantalla / 2,
    location=(0, 0, altura_total)
)
pantalla = bpy.context.active_object
pantalla.name = "PantallaLampara"

bpy.ops.mesh.primitive_cube_add(location=(0, 0, altura_total - diametro_pantalla/2), scale=(diametro_pantalla, diametro_pantalla, diametro_pantalla))
cortador = bpy.context.active_object
cortador.hide_set(True)
mod = pantalla.modifiers.new(name='Boolean', type='BOOLEAN')
mod.object = cortador
mod.operation = 'INTERSECT'

bpy.context.view_layer.objects.active = pantalla
pantalla.select_set(True)
bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.data.objects.remove(cortador, do_unlink=True)

# Luz puntual
bpy.ops.object.light_add(type='POINT', radius=0.2, location=(0, 0, altura_total - 0.1))
bpy.context.object.data.energy = 50
