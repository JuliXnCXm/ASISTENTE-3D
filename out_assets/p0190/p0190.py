import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro = 0.2
altura_cuerpo = 0.9
radio = diametro / 2

# Crear el cuerpo cilíndrico
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio,
    depth=altura_cuerpo,
    location=(0, 0, altura_cuerpo / 2)
)
cuerpo = bpy.context.active_object
cuerpo.name = "CuerpoBolardo"

# Crear la tapa semiesférica (usando una esfera completa posicionada)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio,
    location=(0, 0, altura_cuerpo)
)
tapa = bpy.context.active_object
tapa.name = "TapaBolardo"

# Unir objetos para formar un solo bolardo (opcional pero bueno para la organización)
bpy.context.view_layer.objects.active = cuerpo
cuerpo.select_set(True)
tapa.select_set(True)
bpy.ops.object.join()