import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros de la Pérgola ---
ancho_pergola = 6.0
fondo_pergola = 4.0
alto_pergola = 2.8
grosor_viga = 0.2
alto_columna = 2.5
ancho_columna = 0.25
separacion_columnas = 1.5

# --- Crear Columnas ---
num_columnas_x = int(ancho_pergola / separacion_columnas)
num_columnas_y = 2 # 2 filas

for i in range(num_columnas_x):
    for j in range(num_columnas_y):
        x_pos = -ancho_pergola/2 + separacion_columnas/2 + i * separacion_columnas
        z_pos = alto_columna/2
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_pos, fondo_pergola/2, z_pos),
            scale=(ancho_columna, ancho_columna, alto_columna)
        )
        A.asignar_material(bpy.context.active_object, nombre="Madera_Roble")

# --- Crear Vigas ---
# Viga principal a lo largo de X
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho_pergola/2, 0, alto_pergola + grosor_viga/2),
    scale=(ancho_pergola, fondo_pergola, grosor_viga)
)
A.asignar_material(bpy.context.active_object, nombre="Madera_Roble")

# Viga secundaria a lo largo de Y
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho_pergola/2, fondo_pergola/2, alto_pergola + grosor_viga*1.5),
    scale=(ancho_pergola, grosor_viga, fondo_pergola)
)
A.asignar_material(bpy.context.active_object, nombre="Madera_Roble")

# --- Crear Cubierta Ondulada (con modificador) ---
# Base de la cubierta
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho_pergola/2, 0, alto_pergola + grosor_viga*2),
    scale=(ancho_pergola, fondo_pergola, grosor_viga)
)
cubierta_base = bpy.context.active_object
A.asignar_material(cubierta_base, nombre="Tela_Pergola")

# Modificador de ondulado
oscilacion_z = 0.2
oscilacion_x = 0.1
cubierta_base.modifiers.new(name='Ondulado', type='SIMPLE_DEFORM')
cubierta_base.modifiers['Ondulado'].simple_deform.deformed_depth = oscilacion_z
cubierta_base.modifiers['Ondulado'].simple_deform.deformed_warp = oscilacion_x
cubierta_base.modifiers['Ondulado'].simple_deform.deform_axis = 'Z'

# --- Crear Suelo ---
A.crear_terreno_plano(
    nombre="Suelo_Jardin",
    ancho=10.0,
    fondo=10.0,
    espesor=0.1,
    origen=(0, 0, -0.05),
    material="Cesped"
)