import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

ancho_estudio = 6.0
fondo_estudio = 5.0
alto_estudio = 2.9
grosor_muro = 0.15

estudio = A.crear_habitacion(
    nombre="Estudio",
    ancho=ancho_estudio,
    fondo=fondo_estudio,
    alto=alto_estudio,
    grosor_muro=grosor_muro,
    material_muro="Estuco",
    material_suelo="Ceramica_Piso"
)

cama = A.crear_cama(
    nombre="Cama_Estudio",
    ancho=1.4, largo=2.0, alto_cabecero=1.0,
    origen=(grosor_muro, grosor_muro, 0),
    material_colchon="Textil_Blanco", material_base="Madera"
)

A.crear_armario(
    nombre="Armario_Estudio",
    ancho=1.2, alto=2.4, fondo=0.6,
    origen=(grosor_muro + 1.4 + 0.1, grosor_muro, 0),
    material_cuerpo="MDF_Blanco"
)

mesa_origen = (ancho_estudio / 2.0, fondo_estudio / 2.0 + 0.5, 0)
A.crear_mesa(
    nombre="Mesa_Comedor",
    ancho=0.8, fondo=0.8, alto=0.76,
    origen=mesa_origen,
    material_tablero="Madera_Roble"
)
A.crear_silla(nombre="Silla_1", origen=(mesa_origen[0] - 0.2, mesa_origen[1] - 0.6, 0), material="Madera_Roble")
A.crear_silla(nombre="Silla_2", origen=(mesa_origen[0] + 0.2, mesa_origen[1] + 0.6, 0), material="Madera_Roble")

px = ancho_estudio - grosor_muro
py = fondo_estudio - grosor_muro
perfil_encimera = [
    (px - 2.5, py), (px, py), (px, py - 1.8), 
    (px - 0.6, py - 1.8), (px - 0.6, py - 0.6), (px - 2.5, py - 0.6)
]
A.extruir_perfil(
    nombre="Encimera_Cocina",
    puntos_2d=perfil_encimera,
    altura=0.9,
    material="Porcelanato"
)

A.agregar_luz(nombre="Luz_Area", tipo="AREA", ubicacion=(3, 2.5, 2.8), energia=400)