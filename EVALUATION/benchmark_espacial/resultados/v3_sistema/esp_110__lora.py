import blender_arch as A
A.limpiar_escena()
ancho_total = 18.0
fondo_total = 14.0
alto_piso = 3.0
num_pisos = 3
grosor_muro = 0.25
ancho_brazo_x = 6.0
fondo_brazo_y = 6.0
A.crear_muro(nombre='Muro_Norte', largo=ancho_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(0, fondo_total - grosor_muro / 2, 0), rotacion_z=90)
A.crear_muro(nombre='Muro_Oeste', largo=fondo_brazo_y, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(0, 0, 0), rotacion_z=0)
A.crear_muro(nombre='Muro_Sur', largo=ancho_brazo_x, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(ancho_total - grosor_muro / 2, 0, 0), rotacion_z=-90)
A.crear_muro(nombre='Muro_Este', largo=fondo_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(ancho_total, 0, 0), rotacion_z=0)
muros_edificio = []
for nombre in ['Muro_Norte', 'Muro_Oeste', 'Muro_Sur', 'Muro_Este']:
    for obj in bpy.data.objects:
        if obj.name.startswith(nombre):
            muros_edificio.append(obj)
A.asignar_material('Mat', base_color=(0.1, 0.1, 0.1, 1), roughness=0.5, metallic=0.1, transmission=0, ior=1.5)
for muro in muros_edificio:
    A.asignar_material(muro, nombre='Mat')