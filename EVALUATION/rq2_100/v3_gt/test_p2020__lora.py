import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y MUEBLES ---
ancho_salon = 4.0
fondo_salon = 3.0
alto_salon = 2.8
grosor_muro = 0.15

hab = A.crear_habitacion(
    nombre="Salon",
    ancho=ancho_salon,
    fondo=fondo_salon,
    alto=alto_salon,
    grosor_muro=grosor_muro,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Mueble de TV bajo
mueble_tv = A.crear_armario(
    nombre="Mueble_TV",
    ancho=1.2,
    alto=0.4,
    fondo=0.3,
    num_puertas=1,
    origen=(0, -fondo_salon/2 + 0.3/2 + 0.05, 0),
    material_cuerpo="MDF_Blanco"
)

# --- PARED DE ACCENTO CON LISTONES ---
ancho_liston = 0.02
separacion_liston = 0.01
num_listones = int((ancho_salon - grosor_muro) / (ancho_liston + separacion_liston))

liston = A.crear_losa_rectangular(
    nombre="Liston_Madera",
    ancho=ancho_liston,
    fondo=0.04,
    espesor=0.15,
    origen=(ancho_salon/2 - grosor_muro/2, 0, 0),
    material="Madera_Roble"
)

array_mod = liston.modifiers.new(name='ArrayListones', type='ARRAY')
array_mod.count = num_listones
array_mod.use_relative_offset = False
array_mod.use_object_offset = True
array_mod.offset_object = liston
array_mod.relative_offset_displace[0] = 0
array_mod.relative_offset_displace[1] = 0
array_mod.relative_offset_displace[2] = 0

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz("Luz_Salon", tipo="AREA", ubicacion=(0, 0, alto_salon - 0.1), energia=600)
A.crear_camara("Camara_Salon", ubicacion=(-2, -2, 2), rotacion=(70, 0, 0))