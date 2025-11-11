import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones y posición
diametro = 0.4
altura_lampara = 0.15
altura_suelo = 2.5

# Crear la lámpara
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro / 2,
    depth=altura_lampara,
    location=(0, 0, altura_suelo + altura_lampara / 2),
    vertices=64
)

# Renombrar el objeto
bpy.context.active_object.name = 'LamparaTechoCilindrica'