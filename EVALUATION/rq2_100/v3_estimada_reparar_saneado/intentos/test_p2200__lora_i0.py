import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros de la Pérgola ---
ancho_pergola = 4.0
fondo_pergola = 3.0
alto_pergola = 2.5
dim_columna = 0.25
num_columnas = 4
grosor_viga = 0.15
alto_viga = alto_pergola - grosor_viga
ancho_tela = ancho_pergola * 1.2
fondo_tela = fondo_pergola * 1.2

# --- Crear Columnas ---
espacio_x = (ancho_pergola - dim_columna) / (num_columnas - 1)
for i in range(num_columnas):
    x_pos = -ancho_pergola/2 + espaciodim_columna + i * espacio_x
    A.crear_columna(
        nombre=f"Columna_{i+1}",
        seccion="rect",
        ancho=dim_columna,
        fondo=dim_columna,
        alto=alto_pergola,
        origen=(x_pos, 0, 0),
        material="Madera_Roble"
    )

# --- Crear Vigas ---
A.crear_losa_rectangular(
    nombre="Viga_Principal",
    ancho=ancho_pergola,
    fondo=dim_columna,
    espesor=grosor_viga,
    origen=(-ancho_pergola/2, -dim_columna/2, alto_pergola),
    material="Madera_Roble"
)
A.crear_losa_rectangular(
    nombre="Viga_Secundaria",
    ancho=dim_columna,
    fondo=fondo_pergola,
    espesor=grosor_viga,
    origen=(-dim_columna/2, -fondo_pergola/2, alto_pergola),
    material="Madera_Roble"
)

# --- Crear Cubierta de Tela (con bpy) ---
# Crear el objeto para la tela
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, alto_pergola + 0.1))
tela_obj = bpy.context.active_object
tela_obj.name = "Cubierta_Tela"
tela_obj.dimensions = (ancho_tela, fondo_tela, 0)
A.asignar_material(tela_obj, nombre="Tela_Pergola", base_color=(0.2, 0.2, 0.2, 0.7))

# Crear el modificador de deformación
deform_mod = tela_obj.modifiers.new(name="Ondulado", type='SIMPLE_DEFORM')
deform_mod.deform_method = 'WAVE'
deform_mod.direction = 'Z'
deform_mod.deform_axis = 'X'
deform_mod.strength = 0.05
deform_mod.phase = 0.5
deform_mod.deformed_bounds = (-ancho_tela/2, ancho_tela/2)

# --- Crear Suelo ---
A.crear_terreno_plano(
    nombre="Suelo_Jardin",
    ancho=5.0,
    fondo=5.0,
    espesor=0.1,
    origen=(-2.5, -2.5, -0.1),
    material="Cesped"
)