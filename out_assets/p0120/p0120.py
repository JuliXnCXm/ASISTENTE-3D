import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del cuarto ---
largo = 5.0  # Dimensión en X
ancho = 4.0  # Dimensión en Y
alto = 2.5
espesor = 0.2

# --- Función para crear un muro ---
def crear_muro(nombre, escala, localizacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=localizacion)
    muro = bpy.context.active_object
    muro.name = nombre
    muro.scale = escala
    return muro

# --- Coordenadas y dimensiones de los muros ---
# Muro Norte (al fondo en +Y)
escala_norte = (largo, espesor, alto)
loc_norte = (0, ancho / 2 - espesor / 2, alto / 2)
crear_muro("MuroNorte", escala_norte, loc_norte)

# Muro Sur (al frente en -Y)
escala_sur = (largo, espesor, alto)
loc_sur = (0, -ancho / 2 + espesor / 2, alto / 2)
crear_muro("MuroSur", escala_sur, loc_sur)

# Muro Este (a la derecha en +X)
escala_este = (espesor, ancho - 2 * espesor, alto)
loc_este = (largo / 2 - espesor / 2, 0, alto / 2)
crear_muro("MuroEste", escala_este, loc_este)

# Muro Oeste (a la izquierda en -X)
escala_oeste = (espesor, ancho - 2 * espesor, alto)
loc_oeste = (-largo / 2 + espesor / 2, 0, alto / 2)
crear_muro("MuroOeste", escala_oeste, loc_oeste)