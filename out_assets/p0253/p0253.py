import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de los muros ---
altura = 3.0
espesor = 0.25
largo_norte = 5.0
largo_oeste = 4.0

# --- Creación del muro Norte (a lo largo del eje X) ---
bpy.ops.mesh.primitive_cube_add(
    location=(largo_norte / 2, -espesor / 2, altura / 2)
)
muro_norte = bpy.context.active_object
muro_norte.name = "MuroNorte"
muro_norte.dimensions = (largo_norte, espesor, altura)

# --- Creación del muro Oeste (a lo largo del eje Y) ---
# Se ajusta la posición para que las caras exteriores coincidan en la esquina
bpy.ops.mesh.primitive_cube_add(
    location=(-espesor / 2, largo_oeste / 2 - espesor, altura / 2)
)
muro_oeste = bpy.context.active_object
muro_oeste.name = "MuroOeste"
muro_oeste.dimensions = (espesor, largo_oeste, altura)