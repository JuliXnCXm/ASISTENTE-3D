import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_trasero = 5.0
largo_lateral = 4.0
altura = 2.8
espesor = 0.15

# Crear muro trasero (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_trasero / 2, espesor / 2, altura / 2),
    scale=(largo_trasero, espesor, altura)
)
bpy.context.active_object.name = 'MuroTrasero'

# Crear muro lateral izquierdo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(espesor / 2, (largo_lateral + espesor) / 2, altura / 2),
    scale=(espesor, largo_lateral + espesor, altura)
)
bpy.context.active_object.name = 'MuroLateralIzquierdo'

# Crear muro lateral derecho
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_trasero - espesor / 2, (largo_lateral + espesor) / 2, altura / 2),
    scale=(espesor, largo_lateral + espesor, altura)
)
bpy.context.active_object.name = 'MuroLateralDerecho'