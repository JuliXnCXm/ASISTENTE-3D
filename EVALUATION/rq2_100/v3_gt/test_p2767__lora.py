import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la pérgola ---
ancho = 4.0
fondo = 3.0
alto = 2.8
seccion_poste = 0.15
seccion_viga = (0.1, 0.2)
seccion_vigueta = (0.08, 0.15)

# --- Función auxiliar para crear elementos ---
def crear_barra(nombre, ubicacion, dimensiones):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    barra = bpy.context.active_object
    barra.name = nombre
    barra.dimensions = dimensiones
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return barra

# --- Creación de los postes ---
posiciones_postes = [
    (-ancho/2 + seccion_poste/2, -fondo/2 + seccion_poste/2),
    (ancho/2 - seccion_poste/2, -fondo/2 + seccion_poste/2),
    (-ancho/2 + seccion_poste/2, fondo/2 - seccion_poste/2),
    (ancho/2 - seccion_poste/2, fondo/2 - seccion_poste/2)
]

for i, pos in enumerate(posiciones_postes):
    crear_barra(f"Poste_{i+1}", pos, (seccion_poste, seccion_poste, alto))

# --- Creación de las vigas principales ---
posiciones_vigas = [(0, -fondo/2 + seccion_poste/2), (0, fondo/2 - seccion_poste/2)]
for i, pos in enumerate(posiciones_vigas):
    crear_barra(f"Viga_Principal_{i+1}", pos, (ancho, seccion_viga[1], seccion_viga[0]))

# --- Creación de las viguetas transversales ---
num_viguetas = 5
espaciado_viguetas = ancho / (num_viguetas - 1) if num_viguetas > 1 else 0
for i in range(num_viguetas):
    x_pos = -ancho/2 + seccion_poste/2 + i * espaciado_viguetas
    crear_barra(f"Vigueta_{i+1}", (x_pos, 0, seccion_viga[0]/2 + seccion_vigueta[0]/2), (seccion_vigueta[0], fondo, seccion_vigueta[1]))