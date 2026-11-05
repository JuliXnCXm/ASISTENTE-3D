import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Dimensiones ---
largo = 4.0
ancho = 3.0
alto = 2.5
dim_poste = 0.2
dim_viga_p = 0.2
dim_viga_t = 0.15
num_vigas_t = 5

# --- Crear Postes ---
posiciones_postes = [
    (largo/2, ancho/2, alto/2),
    (-largo/2, ancho/2, alto/2),
    (-largo/2, -ancho/2, alto/2),
    (largo/2, -ancho/2, alto/2)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos, scale=(dim_poste, dim_poste, alto))
    bpy.context.object.name = f"Poste.{i+1:02d}"

# --- Crear Vigas Principales ---
for i in [-1, 1]:
    loc = (0, i * ancho/2, alto + dim_viga_p/2)
    escala = (largo + dim_poste, dim_viga_p, dim_viga_p)
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, scale=escala)
    bpy.context.object.name = f"VigaPrincipal.{i}"
    
# --- Crear Vigas Transversales ---
espaciado = largo / (num_vigas_t - 1) if num_vigas_t > 1 else 0
for i in range(num_vigas_t):
    x_pos = -largo/2 + i * espaciado
    loc = (x_pos, 0, alto + dim_viga_p + dim_viga_t/2)
    escala = (dim_viga_t, ancho + dim_poste, dim_viga_t)
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, scale=escala)
    bpy.context.object.name = f"VigaTransversal.{i+1:02d}"