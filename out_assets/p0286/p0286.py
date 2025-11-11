import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro = 0.15
altura = 0.80
radio = diametro / 2

# Crear el cuerpo de la baliza
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio,
    depth=altura,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, altura / 2),
    vertices=32
)
baliza = bpy.context.active_object
baliza.name = 'CuerpoBaliza'

# Crear la fuente de luz
luz_loc_z = altura - 0.10
bpy.ops.object.light_add(
    type='POINT',
    radius=0.1,
    align='WORLD',
    location=(0, 0, luz_loc_z)
)
luz = bpy.context.active_object
luz.name = 'LuzBaliza'
luz.data.energy = 50 # Watts