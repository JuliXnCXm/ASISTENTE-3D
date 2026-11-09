import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho = 12.0
fondo = 8.0
alto_piso = 3.0
grosor_muro = 0.25
voladizo = 0.5
altura_cumbrera = 2.0
angulo_cumbrera = 10.0

# Crear el volumen exterior
A.crear_habitacion(
    nombre="Casa",
    ancho=ancho,
    fondo=fondo,
    alto=alto_piso + altura_cumbrera,
    grosor_muro=grosor_muro,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Concreto_Piso",
    material_techo="Teja"
)

# Crear el techo con bpy
A.extruir_techo_con_pendientes(
    nombre="Techo_Cumbrera",
    ancho=ancho,
    fondo=fondo,
    altura_cumbrera=altura_cumbrera,
    voladizo_x=voladizo,
    voladizo_y=voladizo,
    angulo_x=angulo_cumbrera,
    origen=(0, 0, alto_piso),
    material="Teja"
)