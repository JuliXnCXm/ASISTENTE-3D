import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del objeto ---
largo = 6.0
ancho = 4.0
espesor = 0.2

# --- Creación de la losa ---
# Se crea un cubo y se ajustan sus dimensiones y posición
# La posición en Z es -espesor/2 para que la cara superior quede en Z=0
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo / 2, ancho / 2, -espesor / 2),
    scale=(largo, ancho, espesor)
)

# --- Nombrar el objeto ---
bpy.context.object.name = 'Losa_Suelo'