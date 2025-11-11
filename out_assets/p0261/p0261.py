import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

altura_cuerpo = 0.9
radio_cuerpo = 0.15

# Cuerpo
bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,
    radius=radio_cuerpo,
    depth=altura_cuerpo,
    location=(0, 0, altura_cuerpo / 2)
)
cuerpo = bpy.context.active_object
cuerpo.name = "CuerpoBolardo"

# Cabeza semiesférica
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=32,
    ring_count=16,
    radius=radio_cuerpo,
    location=(0, 0, altura_cuerpo)
)
cabeza = bpy.context.active_object
cabeza.name = "CabezaBolardo"

# Unir correctamente (sin override de contexto)
bpy.ops.object.select_all(action='DESELECT')
cuerpo.select_set(True)
cabeza.select_set(True)
bpy.context.view_layer.objects.active = cuerpo
bpy.ops.object.join()
