import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_asiento = 2.0
ancho_asiento = 0.4
grosor_asiento = 0.05
altura_asiento = 0.45
tamano_pata = 0.4
separacion_patas = 1.4

# Crear el asiento
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, altura_asiento + grosor_asiento / 2),
    scale=(largo_asiento / 2, ancho_asiento / 2, grosor_asiento / 2)
)
asiento_obj = bpy.context.active_object
asiento_obj.name = "AsientoBanco"

# Crear pata 1
bpy.ops.mesh.primitive_cube_add(
    size=tamano_pata,
    location=(-separacion_patas / 2, 0, tamano_pata / 2)
)
pata1_obj = bpy.context.active_object
pata1_obj.name = "PataBanco.001"

# Crear pata 2
bpy.ops.mesh.primitive_cube_add(
    size=tamano_pata,
    location=(separacion_patas / 2, 0, tamano_pata / 2)
)
pata2_obj = bpy.context.active_object
pata2_obj.name = "PataBanco.002"