import blender_arch as A

A.limpiar_escena()

ancho = 4.0
fondo = 3.0
alto = 2.5
grosor = 0.15

# Muros
muro_frontal = A.crear_muro("MuroFrontal", largo=ancho, alto=alto, grosor=grosor, origen=(-ancho/2, -fondo/2, 0), material="Estuco")
muro_trasero = A.crear_muro("MuroTrasero", largo=ancho, alto=alto, grosor=grosor, origen=(-ancho/2, fondo/2, 0), material="Estuco")
muro_izq = A.crear_muro("MuroIzq", largo=fondo, alto=alto, grosor=grosor, origen=(-ancho/2, -fondo/2, 0), rotacion_z=90, material="Estuco")
muro_der = A.crear_muro("MuroDer", largo=fondo, alto=alto, grosor=grosor, origen=(ancho/2, -fondo/2, 0), rotacion_z=90, material="Estuco")

# Suelo
A.crear_piso("Suelo", ancho=ancho, fondo=fondo, espesor=0.05, origen=(-ancho/2, -fondo/2, 0), material="Ceramica_Piso")

# Puerta en el muro frontal
ancho_puerta = 0.9
alto_puerta = 2.1

centro_puerta = (0, -fondo/2, alto_puerta / 2)

A.crear_puerta(
    "PuertaAcceso",
    ancho=ancho_puerta,
    alto=alto_puerta,
    prof_marco=grosor,
    origen=(centro_puerta[0] - ancho_puerta/2, centro_puerta[1], 0),
    material_panel="Madera",
    material_marco="Marco_Blanco"
)

# Abrir vano para la puerta
A.abrir_vanos_batch_rectangulares(
    muro_frontal,
    centros_world=[centro_puerta],
    ancho=ancho_puerta,
    alto=alto_puerta
)