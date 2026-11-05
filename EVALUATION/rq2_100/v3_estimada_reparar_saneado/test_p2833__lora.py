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
dim_viga_principal = (0.15, 0.15, 0.25)
dim_vigueta_transversal = (0.1, 0.15, 0.1)

# --- Función para crear un objeto 3D ---
def crear_objeto(nombre, ubicacion, dimensiones):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.dimensions = dimensiones
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

# --- Crear Postes ---
posiciones_postes = [
    (largo_pergola / 2, ancho_pergola / 2, alto_pergola / 2),
    (-largo_pergola / 2, ancho_pergola / 2, alto_pergola / 2),
    (largo_pergola / 2, -ancho_pergola / 2, alto_pergola / 2),
    (-largo_pergola / 2, -ancho_pergola / 2, alto_pergola / 2)
]
for i, pos in enumerate(posiciones_postes):
    crear_objeto(f"Poste_{i+1}", pos, (lado_poste, lado_poste, alto_pergola))

# --- Crear Vigas Principales ---
posiciones_vigas_principales = [
    (0, ancho_pergola / 2, alto_pergola + dim_viga_principal[2] / 2),
    (0, -ancho_pergola / 2, alto_pergola + dim_viga_principal[2] / 2)
]
for i, pos in enumerate(posiciones_vigas_principales):
    crear_objeto(f"Viga_Principal_{i+1}", pos, (largo_pergola, lado_poste, dim_viga_principal[2]))

# --- Crear Viguetas Transversales ---
num_viguetas = 5
espaciado_viguetas = largo_pergola / (num_viguetas - 1) if num_viguetas > 1 else 0
for i in range(num_viguetas):
    pos_x = -largo_pergola / 2 + i * espaciado_viguetas
    crear_objeto(f"Vigueta_{i+1}", (pos_x, 0, alto_pergola + dim_viga_principal[2] + dim_vigueta_transversal[2] / 2), dim_vigueta_transversal)