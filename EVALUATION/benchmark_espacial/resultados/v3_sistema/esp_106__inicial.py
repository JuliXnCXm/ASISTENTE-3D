import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho = 10.0
fondo = 10.0
alto_piso = 3.0
grosor_muro = 0.25
altura_cumbrera = 2.0
angulo_cumbrera = 10.0 # En grados

# Crear el volumen exterior
vol_casa = A.crear_habitacion(
    nombre="CasaMonoPendiente",
    ancho=ancho,
    fondo=fondo,
    alto=alto_piso + altura_cumbrera,
    grosor_muro=grosor_muro,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Concreto_Piso",
    material_techo="Teja"
)

# Crear el techo usando un cubo y una escala
vol_techo = A.crear_cubo(
    nombre="TechoMonoPendiente",
    ancho=ancho,
    fondo=fondo,
    alto=altura_cumbrera,
    origen=(0, 0, alto_piso),
    material="Teja"
)
vol_techo.rotation_euler[2] = -angulo_cumbrera * 3.14159 / 180 # De grados a radianes

# Aplicar modificador booleano para cortar el techo en el hueco
mod_bool = vol_techo.modifiers.new(name='BooleanHueco', type='BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = vol_casa
A.asignar_modificador_boolean(vol_techo, mod_bool)