import blender_arch as A
A.limpiar_escena()
ancho = 8.0
fondo = 8.0
alto_piso = 3.0
num_pisos = 2
grosor_muro = 0.25
voladizo = 0.5
vol_x = ancho + 2 * grosor_muro
vol_y = fondo + 2 * grosor_muro
vol_z = alto_piso * num_pisos
exterior = A.crear_volumen(nombre='Casa', dimensiones=(vol_x, vol_y, vol_z), material='Muro_Pintura')
for i in range(num_pisos):
    z_piso = i * alto_piso
    A.crear_losa_rectangular(nombre=f'Piso_{i + 1}', ancho=ancho, fondo=fondo, espesor=0.2, origen=(0, 0, z_piso), material='Concreto_Piso')
techo_z = vol_z - 0.2
A.crear_techo_plano(nombre='Techo', ancho=ancho, fondo=fondo, espesor=0.2, origen=(0, 0, techo_z), material='Teja')
A.extruir_con_huecos(nombre='Tejado', contorno=[(-vol_x / 2, -vol_y / 2), (vol_x / 2, -vol_y / 2), (vol_x / 2, vol_y / 2), (-vol_x / 2, vol_y / 2)], agujeros=[[(-vol_x / 2, -vol_y / 2), (vol_x / 2, -vol_y / 2), (vol_x / 2, vol_y / 2), (-vol_x / 2, vol_y / 2)]], altura=techo_z, material='Teja')
A.asignar_material(exterior, nombre='Mat')
A.crear_muro(nombre='Muro_Frontal', largo=vol_x, alto=alto_piso, grosor=grosor_muro, origen=(0, 0, 0), rotacion_z=-90, material='Muro_Pintura')