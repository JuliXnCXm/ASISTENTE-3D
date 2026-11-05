import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros de la Pérgola ---
ancho = 6.0
fondo = 4.0
alto = 2.8
grosor_poste = 0.2
grosor_viga = 0.2
alto_viga = 0.2
ancho_tela = 7.0
fondo_tela = 5.0
altura_tela = 2.5
voladizo = 0.5

# --- Crear Columnas ---
pos_x = ancho / 2 - grosor_poste / 2
pos_y = fondo / 2 - grosor_poste / 2
for i in [-1, 1]:
    for j in [-1, 1]:
        x = pos_x * i
        y = pos_y * j
        A.crear_columna(
            nombre=f"Poste_{i}_{j}",
            seccion="rect",
            ancho=grosor_poste,
            fondo=grosor_poste,
            alto=alto,
            origen=(x, y, 0),
            material="Madera_Roble"
        )

# --- Crear Vigas ---
A.crear_losa_rectangular(
    nombre="Viga_Principal_1",
    ancho=ancho + voladizo,
    fondo=grosor_viga,
    espesor=alto_viga,
    origen=(-voladizo/2, -fondo/2, alto),
    material="Madera_Roble"
)
A.crear_losa_rectangular(
    nombre="Viga_Principal_2",
    ancho=ancho + voladizo,
    fondo=grosor_viga,
    espesor=alto_viga,
    origen=(-voladizo/2, fondo/2 - grosor_viga, alto),
    material="Madera_Roble"
)

# --- Crear Cubierta de Tela ---
# Crear el contenedor para la tela
A.crear_losa_rectangular(
    nombre="Soporte_Tela",
    ancho=ancho_tela,
    fondo=fondo_tela,
    espesor=0.01,
    origen=(0, 0, altura_tela),
    material="Tela_Blanca"
)

# Crear la tela ondulada
num_picos = 10
for i in range(num_picos):
    x = (i / num_picos) * ancho_tela
    z = (i / num_picos) * (ancho_tela / 2) # Ondulación simple
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0, z))
    tela = bpy.context.active_object
    tela.name = f"Tela_Pico_{i}"
    tela.scale.x = ancho_tela / num_picos
    tela.scale.y = fondo_tela
    A.asignar_material(tela, nombre="Tela_Blanca", base_color=(0.9, 0.9, 1.0, 1.0))