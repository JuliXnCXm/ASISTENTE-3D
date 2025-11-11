import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura = 2.7
espesor = 0.15
largo_trasero = 5.0
largo_lateral = 4.0

# Crear muro trasero (Norte)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_trasero / 2, largo_lateral - espesor / 2, altura / 2),
    scale=(largo_trasero, espesor, altura)
)
bpy.context.active_object.name = "MuroNorte"

# Crear muro lateral (Oeste)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(espesor / 2, largo_lateral / 2, altura / 2),
    scale=(espesor, largo_lateral, altura)
)
bpy.context.active_object.name = "MuroOeste"

# Crear muro lateral (Este)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_trasero - espesor / 2, largo_lateral / 2, altura / 2),
    scale=(espesor, largo_lateral, altura)
)
bpy.context.active_object.name = "MuroEste"