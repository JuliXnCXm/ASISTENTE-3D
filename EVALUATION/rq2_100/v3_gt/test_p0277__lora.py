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
alto_viga_principal = 0.15
dim_viga_principal = 0.15
alto_viga_transversal = 0.10
dim_viga_transversal = 0.10
num_vigas_transversales = 5

# --- Función para crear un objeto sólido ---
def crear_objeto_solido(nombre, dimensiones, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.dimensions = dimensiones
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

# --- Crear postes ---
posiciones_postes = [
    (-ancho/2, -fondo/2, alto_poste/2),
    (ancho/2, -fondo/2, alto_poste/2),
    (-ancho/2, fondo/2, alto_poste/2),
    (ancho/2, fondo/2, alto_poste/2)
]
for i, pos in enumerate(posiciones_postes):
    crear_objeto_solido(f"Poste_{i+1}", (dim_poste, dim_poste, alto_poste), pos)

# --- Crear vigas principales ---
posiciones_vigas_principales = [
    (-ancho/2, 0, alto_poste + alto_viga_principal/2),
    (ancho/2, 0, alto_poste + alto_viga_principal/2)
]
for i, pos in enumerate(posiciones_vigas_principales):
    crear_objeto_solido(f"Viga_Principal_{i+1}", (ancho + dim_poste, dim_viga_principal, alto_viga_principal), pos)

# --- Crear vigas transversales ---
espaciado = ancho / (num_vigas_transversales - 1) if num_vigas_transversales > 1 else 0
for i in range(num_vigas_transversales):
    x_pos = -ancho/2 + i * espaciado
    crear_objeto_solido(f"Viga_Transversal_{i+1}", (dim_viga_transversal, fondo + dim_poste, alto_viga_transversal), (x_pos, 0, alto_poste + alto_viga_principal + alto_viga_transversal/2))