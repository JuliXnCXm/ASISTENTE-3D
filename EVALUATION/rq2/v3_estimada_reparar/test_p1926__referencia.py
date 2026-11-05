import blender_arch as A
import bpy

A.limpiar_escena()

# --- HABITACION Y SILLA (DSL) ---
habitacion = A.crear_habitacion('Oficina', ancho=3.5, fondo=3, alto=2.6, grosor_muro=0.1, material_suelo='Concreto_Piso', material_muro='Muro_Pintura_Gris')
silla = A.crear_silla('Silla_Oficina', origen=(1.5, 1.5, 0), material='Cuero')

# --- ESCRITORIO DE ESQUINA PERSONALIZADO (BPY) ---
# Crear un perfil en L para la tabla del escritorio
perfil_L = [
    (0, 0), (2.5, 0), (2.5, 0.6), (0.6, 0.6), (0.6, 1.8), (0, 1.8)
]

# Extruir el perfil para crear el escritorio
escritorio = A.extruir_perfil('Escritorio', puntos_2d=perfil_L, altura=0.04, material='Madera_Roble')
escritorio.location = (0.1, 0.1, 0.75) # Mover a la esquina y a la altura correcta

# Crear patas metálicas cilíndricas con un bucle
patas_pos = [(0.2, 0.2, 0), (2.3, 0.2, 0), (0.2, 1.6, 0)]
for i, pos in enumerate(patas_pos):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.75, location=(pos[0]+0.1, pos[1]+0.1, 0.75/2))
    pata = bpy.context.active_object
    pata.name = f'Pata_{i+1}'
    A.asignar_material(pata, 'Acero_Inox')

# --- LIBRERIA PARAMETRICA (BPY) ---
ancho_libreria = 2.0
alto_libreria = 2.4
fondo_libreria = 0.3
espesor_panel = 0.02
num_verticales = 4
num_horizontales = 6

origen_libreria = (3.5 - 0.1 - fondo_libreria, 0.5, 0)

# Paneles verticales
dx = ancho_libreria / (num_verticales - 1)
for i in range(num_verticales):
    x = origen_libreria[0]
    y = origen_libreria[1] + i * dx
    z = origen_libreria[2] + alto_libreria / 2
    bpy.ops.mesh.primitive_cube_add(location=(x + fondo_libreria/2, y, z))
    panel_v = bpy.context.active_object
    panel_v.name = f'Vertical_{i}'
    panel_v.dimensions = (fondo_libreria, espesor_panel, alto_libreria)
    A.asignar_material(panel_v, 'Madera_Roble')

# Paneles horizontales
dz = alto_libreria / (num_horizontales - 1)
for i in range(num_horizontales):
    x = origen_libreria[0]
    y = origen_libreria[1] + ancho_libreria / 2
    z = origen_libreria[2] + i * dz
    bpy.ops.mesh.primitive_cube_add(location=(x + fondo_libreria/2, y - espesor_panel/2, z))
    panel_h = bpy.context.active_object
    panel_h.name = f'Horizontal_{i}'
    panel_h.dimensions = (fondo_libreria, ancho_libreria, espesor_panel)
    A.asignar_material(panel_h, 'Madera_Roble')

A.agregar_luz('Luz_Oficina', tipo='AREA', ubicacion=(1.75, 1.5, 2.4), energia=300)