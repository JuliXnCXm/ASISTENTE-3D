import blender_arch as A
A.limpiar_escena()
ancho_torre = 30.0
alto_piso = 3.5
num_pisos = 20
grosor_muro = 0.4
A.abrir_vanos_batch_rectangulares('Corte_Nucleo', centros_world=[(0, 0, alto_piso * num_pisos / 2)], ancho=10.0, alto=10.0)
A.extruir_con_huecos('Nucleo_Hormigon', contorno=[[-5, -5], [5, -5], [5, 5], [-5, 5]], agujeros=['Corte_Nucleo'], altura=alto_piso * num_pisos)
for i in range(4):
    x = -5 + i % 2 * 6
    y = -5 + int(i / 2) * 6
    A.crear_columna(f'Columna_{i}', seccion='rect', ancho=0.4, fondo=0.4, alto=alto_piso * num_pisos, origen=(x, y, 0), material='Hormigon')
muro_exterior = A.crear_muro('Muro_Exterior', largo=ancho_torre, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(-ancho_torre / 2, -ancho_torre / 2, 0), material='Vidrio')
muro_interior = A.crear_muro('Muro_Interior', largo=ancho_torre, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(-ancho_torre / 2, -ancho_torre / 2, 0), rotacion_z=180, material='Marco_Negro')