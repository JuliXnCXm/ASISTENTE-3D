import blender_arch as A
import bpy

A.limpiar_escena()

# 1. Base del jardín y materiales
terreno = A.crear_piso('Piso_Jardin', ancho=8, fondo=8, espesor=0.1, origen=(-4, -4, -0.1), material='Cesped')

# 2. Estructura de la pérgola con blender_arch
ANCHO_PERGOLA = 4.0
FONDO_PERGOLA = 3.0
H_PERGOLA = 2.8

# Columnas
posiciones_columnas = [
    (-ANCHO_PERGOLA/2, -FONDO_PERGOLA/2, 0),
    (ANCHO_PERGOLA/2, -FONDO_PERGOLA/2, 0),
    (ANCHO_PERGOLA/2, FONDO_PERGOLA/2, 0),
    (-ANCHO_PERGOLA/2, FONDO_PERGOLA/2, 0)
]
for i, pos in enumerate(posiciones_columnas):
    A.crear_columna(f'Columna.{i}', seccion='rect', ancho=0.2, fondo=0.2, alto=H_PERGOLA, origen=pos, material='Madera_Roble')

# Vigas principales (a lo largo de Y)
A.crear_losa_rectangular('Viga.Principal.1', ancho=0.2, fondo=FONDO_PERGOLA, espesor=0.2, origen=(-ANCHO_PERGOLA/2, -FONDO_PERGOLA/2, H_PERGOLA), material='Madera_Roble')
A.crear_losa_rectangular('Viga.Principal.2', ancho=0.2, fondo=FONDO_PERGOLA, espesor=0.2, origen=(ANCHO_PERGOLA/2 - 0.2, -FONDO_PERGOLA/2, H_PERGOLA), material='Madera_Roble')

# Vigas secundarias (a lo largo de X)
for i in range(5):
    y_pos = -FONDO_PERGOLA/2 + i * (FONDO_PERGOLA / 4)
    A.crear_losa_rectangular(f'Viga.Secundaria.{i}', ancho=ANCHO_PERGOLA, fondo=0.15, espesor=0.15, origen=(-ANCHO_PERGOLA/2, y_pos, H_PERGOLA + 0.2), material='Madera_Roble')

# 3. Cubierta de tela ondulada con bpy
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, H_PERGOLA + 0.3))
canopy = bpy.context.active_object
canopy.name = 'Cubierta_Tela'
canopy.scale.x = ANCHO_PERGOLA
canopy.scale.y = FONDO_PERGOLA

# Añadir subdivisiones para la deformación
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=50)
bpy.ops.object.mode_set(mode='OBJECT')

# Modificador de onda
wave_mod = canopy.modifiers.new(name='Wave', type='WAVE')
wave_mod.height = 0.15
wave_mod.width = 1.0
wave_mod.use_normal = True
wave_mod.use_x = True
wave_mod.use_y = False

# Modificador para dar grosor
solidify_mod = canopy.modifiers.new(name='Solidify', type='SOLIDIFY')
solidify_mod.thickness = 0.01

A.asignar_material(canopy, nombre='TelaBlanca', base_color=(0.9, 0.9, 0.85, 1.0))