import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura principal con blender_arch ---
ancho_loft = 8.0
fondo_loft = 10.0
alto_loft = 5.5

A.crear_piso('Piso_Loft', ancho=ancho_loft, fondo=fondo_loft, espesor=0.15, material='Concreto_Piso')
A.crear_muro('Muro_Fondo', largo=ancho_loft, alto=alto_loft, origen=(0, fondo_loft/2, 0), rotacion_z=180, material='Ladrillo_Rojo')
A.crear_muro('Muro_Izquierdo', largo=fondo_loft, alto=alto_loft, origen=(-ancho_loft/2, 0, 0), rotacion_z=-90, material='Ladrillo_Rojo')

# Mezzanine
ancho_mezzanine = ancho_loft
fondo_mezzanine = 4.0
alto_mezzanine = 2.8

A.crear_losa_rectangular('Losa_Mezzanine', ancho=ancho_mezzanine, fondo=fondo_mezzanine, espesor=0.2, origen=(0, fondo_loft/2 - fondo_mezzanine/2, alto_mezzanine), material='Madera_Roble')
A.crear_columna('Columna_1', seccion='rect', ancho=0.3, fondo=0.3, alto=alto_mezzanine, origen=(-ancho_loft/4, fondo_loft/2 - fondo_mezzanine + 0.15, 0), material='Acero')
A.crear_columna('Columna_2', seccion='rect', ancho=0.3, fondo=0.3, alto=alto_mezzanine, origen=(ancho_loft/4, fondo_loft/2 - fondo_mezzanine + 0.15, 0), material='Acero')

# --- Baranda personalizada con bpy ---
altura_baranda = 1.05

# Postes
for i, x_pos in enumerate([-ancho_loft/2 + 0.15, -2.5, 0, 2.5, ancho_loft/2 - 0.15]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, fondo_loft/2 - fondo_mezzanine, alto_mezzanine + 0.2 + altura_baranda/2))
    poste = bpy.context.active_object
    poste.name = f'Poste_Baranda_{i}'
    poste.scale = (0.05, 0.05, altura_baranda)
    A.asignar_material(poste, nombre="Mat_Acero_Negro", base_color=(0.1, 0.1, 0.1, 1))

# Malla metálica
coord_y_malla = fondo_loft/2 - fondo_mezzanine
z_malla = alto_mezzanine + 0.2 + altura_baranda/2

bpy.ops.mesh.primitive_plane_add(size=1, location=(0, coord_y_malla, z_malla))
malla = bpy.context.active_object
malla.name = 'Malla_Metalica'
malla.scale = (ancho_loft, altura_baranda, 1)

# Modificador Wireframe para crear la malla
mod_wire = malla.modifiers.new(name='Wireframe', type='WIREFRAME')
mod_wire.thickness = 0.015
mod_wire.use_replace = True
mod_wire.use_boundary = True

# Modificador Solidify para dar volumen a los hilos
mod_solid = malla.modifiers.new(name='Solidify', type='SOLIDIFY')
mod_solid.thickness = 0.01

A.asignar_material(malla, nombre="Mat_Acero_Negro", base_color=(0.1, 0.1, 0.1, 1))

# Pasamanos
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, coord_y_malla, alto_mezzanine + 0.2 + altura_baranda))
pasamanos = bpy.context.active_object
pasamanos.name = 'Pasamanos'
pasamanos.scale = (ancho_loft, 0.08, 0.05)
A.asignar_material(pasamanos, nombre="Mat_Madera_Baranda", base_color=(0.3, 0.15, 0.05, 1))

A.crear_camara('Camara_Loft', ubicacion=(-5, -6, 4), rotacion=(70, 0, -30))