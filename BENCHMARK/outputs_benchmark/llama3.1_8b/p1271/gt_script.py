import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_terreno_plano(
    nombre="Parcela",
    ancho=25.0,
    fondo=20.0,
    espesor=0.3,
    origen=(-12.5, -10, -0.3),
    material="Cesped"
)

A.crear_casa_n_pisos(
    nombre="Vivienda_Unifamiliar",
    pisos=1,
    ancho=12.0,
    fondo=9.0,
    alto_piso=3.0,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    origen=(-6, -4.5, 0),
    material_muro="Ladrillo_Rojo",
    material_tejado="Teja"
)

A.crear_arbol_simple(
    nombre="Arbol_Frontal",
    radio_copa=2.5,
    altura_copa=4.0,
    altura_tronco=2.2,
    origen=(3, -7, 0)
)