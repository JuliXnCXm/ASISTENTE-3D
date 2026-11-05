import blender_arch as A
A.limpiar_escena()

# --- Parámetros ---
ancho_torre = 30.0
alto_piso = 3.5
num_pisos = 20
grosor_muro = 0.4

# --- Estructura de Hormigón ---
# Núcleo central
A.crear_hueco('Corte_Nucleo', ancho=10.0, fondo=10.0, alto=num_pisos * alto_piso)
A.extruir_con_huecos('Nucleo_Hormigon', contorno=[[-5, -5], [5, -5], [5, 5], [-5, 5]], agujeros=['Corte_Nucleo'], altura=num_pisos * alto_piso)

# Columnas perimetrales
for i in range(4):
    x = -5 + (i % 2) * 6
    y = -5 + int(i/2) * 6
    A.crear_columna(f'Columna_{i}', seccion='rect', ancho=0.4, fondo=0.4, alto=num_pisos * alto_piso, origen=(x, y, 0), material='Hormigon')

# --- Muro Cortina ---
# Muro exterior
muro_exterior = A.crear_muro('Muro_Exterior', largo=ancho_torre, alto=num_pisos * alto_piso, grosor=grosor_muro, origen=(-ancho_torre/2, -ancho_torre/2, 0), material='Vidrio')
# Muro interior
muro_interior = A.crear_muro('Muro_Interior', largo=ancho_torre, alto=num_pisos * alto_piso, grosor=grosor_muro, origen=(-ancho_torre/2, -ancho_torre/2, 0), rotacion_z=180, material='Marco_Negro')