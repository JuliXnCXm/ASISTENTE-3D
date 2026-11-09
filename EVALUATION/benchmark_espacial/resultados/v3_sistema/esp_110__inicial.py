import blender_arch as A

A.limpiar_escena()

# Dimensiones generales
ancho_total = 18.0
fondo_total = 14.0
alto_piso = 3.0
num_pisos = 3
grosor_muro = 0.25

# Dimensiones de los brazos
ancho_brazo_x = 6.0
fondo_brazo_y = 6.0

# Crear el primer brazo (en eje X)
A.crear_muro(nombre="Muro_Norte", largo=ancho_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(0, fondo_total - grosor_muro/2, 0), rotacion_z=90)
A.crear_muro(nombre="Muro_Oeste", largo=fondo_brazo_y, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(0, 0, 0), rotacion_z=0)

# Crear el segundo brazo (en eje Y)
A.crear_muro(nombre="Muro_Sur", largo=ancho_brazo_x, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(ancho_total - grosor_muro/2, 0, 0), rotacion_z=-90)
A.crear_muro(nombre="Muro_Este", largo=fondo_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(ancho_total, 0, 0), rotacion_z=0)

# Unir todos los muros en un solo objeto
muros_edificio = [obj for nombre in ["Muro_Norte", "Muro_Oeste", "Muro_Sur", "Muro_Este"] for obj in bpy.data.objects if obj.name.startswith(nombre)]
A.unir_objetos(muros_edificio, nombre="Edificio_L")