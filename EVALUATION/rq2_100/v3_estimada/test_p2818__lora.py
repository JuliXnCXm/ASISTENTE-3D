import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la pérgola ---
ancho = 4.0
fondo = 3.0
alto_poste = 2.5
dim_poste = 0.2
num_vigas = 2
num_viguetas = 7
dim_viga = 0.15
dim_vigueta = 0.08

# --- Función auxiliar para crear elementos ---
def crear_cubo(nombre, dimensiones, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.dimensions = dimensiones
    return obj

# --- Crear Postes ---
posiciones_postes = [
    (-ancho/2 + dim_poste/2, -fondo/2 + dim_poste/2, alto_poste/2),
    (ancho/2 - dim_poste/2, -fondo/2 + dim_poste/2, alto_poste/2),
    (-ancho/2 + dim_poste/2, fondo/2 - dim_poste/2, alto_poste/2),
    (ancho/2 - dim_poste/2, fondo/2 - dim_poste/2, alto_poste/2)
]
for i, pos in enumerate(posiciones_postes):
    crear_cubo(f"Poste_{i+1}", (dim_poste, dim_poste, alto_poste), pos)

# --- Crear Vigas Principales ---
posiciones_vigas = [(0, -fondo/2 + dim_poste/2, alto_poste + dim_viga/2), 
                     (0, fondo/2 - dim_poste/2, alto_poste + dim_viga/2)]
for i, pos in enumerate(posiciones_vigas):
    crear_cubo(f"Viga_Prin_{i+1}", (ancho + dim_poste, dim_viga, dim_viga), pos)

# --- Crear Emparrillado Superior ---
espaciado_viguetas = ancho / (num_viguetas - 1) if num_viguetas > 1 else 0
for i in range(num_viguetas):
    x_pos = -ancho/2 + espaciado_viguetas * i
    z_pos = alto_poste + dim_viga + dim_vigueta/2
    crear_cubo(f"Vigueta_{i+1}", (dim_vigueta, ancho + dim_poste, dim_vigueta), (x_pos, 0, z_pos))