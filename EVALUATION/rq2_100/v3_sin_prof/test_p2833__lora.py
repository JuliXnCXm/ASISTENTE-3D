import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la pérgola ---
largo_pergola = 4.0
ancho_pergola = 3.0
alto_pergola = 2.8
lado_poste = 0.15
dim_viga_principal = (0.15, 0.15)
dim_vigueta_transversal = (0.1, 0.15)
num_viguetas = 5

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
    (-largo_pergola/2 + lado_poste/2, -ancho_pergola/2 + lado_poste/2, alto_pergola/2),
    (largo_pergola/2 - lado_poste/2, -ancho_pergola/2 + lado_poste/2, alto_pergola/2),
    (-largo_pergola/2 + lado_poste/2, ancho_pergola/2 - lado_poste/2, alto_pergola/2),
    (largo_pergola/2 - lado_poste/2, ancho_pergola/2 - lado_poste/2, alto_pergola/2)
]
for i, pos in enumerate(posiciones_postes):
    crear_barra(f"Poste_{i+1}", pos, (lado_poste, lado_poste, alto_pergola))

# --- Creación de las vigas principales ---
posiciones_vigas = [
    (-largo_pergola/2 + dim_viga_principal[0]/2, 0, alto_pergola + dim_viga_principal[1]/2),
    (largo_pergola/2 - dim_viga_principal[0]/2, 0, alto_pergola + dim_viga_principal[1]/2)
]
for i, pos in enumerate(posiciones_vigas):
    crear_barra(f"Viga_Principal_{i+1}", pos, dim_viga_principal)

# --- Creación de las viguetas transversales ---
espaciado_viguetas = largo_pergola / (num_viguetas - 1)
for i in range(num_viguetas):
    pos_x = -largo_pergola/2 + i * espaciado_viguetas
    crear_barra(f"Vigueta_{i+1}", (pos_x, 0, alto_pergola + dim_vigueta_transversal[1]/2), dim_vigueta_transversal)