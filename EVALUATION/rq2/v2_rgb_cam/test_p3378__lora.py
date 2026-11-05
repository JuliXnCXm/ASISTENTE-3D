import blender_arch as A
A.limpiar_escena()

# --- Parámetros ---
ancho_piso = 7.0
fondo_piso = 9.0
alto_piso = 2.8
grosor_muro = 0.2

# --- Estructura y mobiliario planta baja ---
piso_0 = A.crear_piso('Piso_Baja', ancho=ancho_piso, fondo=fondo_piso, espesor=0.05, origen=(0,0,-0.05), material='Concreto_Piso')
muro_frente_baja = A.crear_muro('Muro_Frente_Baja', largo=ancho_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,0,0), material='Muro_Pintura_Gris')
muro_fondo_baja = A.crear_muro('Muro_Fondo_Baja', largo=ancho_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,fondo_piso,0), material='Muro_Pintura_Gris')
muro_izq_baja = A.crear_muro('Muro_Izq_Baja', largo=fondo_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,0,0), rotacion_z=90, material='Muro_Pintura_Gris')
muro_der_baja = A.crear_muro('Muro_Der_Baja', largo=fondo_piso, alto=alto_piso, grosor=grosor_muro, origen=(ancho_piso,0,0), rotacion_z=90, material='Muro_Pintura_Gris')

# Mobiliario
sofa = A.crear_sofa('Sofa', ancho=2.5, fondo=0.9, origen=(1.25, 1.5, 0), material='Tela_Gris')
mesa_comedor = A.crear_mesa('Mesa_Comedor', ancho=1.8, fondo=0.9, alto=0.75, origen=(2.5, 6.5, 0), material_tablero='Madera_Roble')
armario = A.crear_armario('Armario', ancho=2.0, alto=2.4, fondo=0.6, origen=(ancho_piso-2.0-0.1, 0.1, 0), material_cuerpo='MDF_Blanco')

# --- Estructura y mobiliario planta alta ---
piso_1 = A.crear_piso('Piso_Alta', ancho=ancho_piso, fondo=fondo_piso, espesor=0.05, origen=(0,0,-0.05), material='Concreto_Piso')
muro_frente_alta = A.crear_muro('Muro_Frente_Alta', largo=ancho_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,0,0), material='Muro_Pintura_Gris')
muro_fondo_alta = A.crear_muro('Muro_Fondo_Alta', largo=ancho_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,fondo_piso,0), material='Muro_Pintura_Gris')
muro_izq_alta = A.crear_muro('Muro_Izq_Alta', largo=fondo_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,0,0), rotacion_z=90, material='Muro_Pintura_Gris')
muro_der_alta = A.crear_muro('Muro_Der_Alta', largo=fondo_piso, alto=alto_piso, grosor=grosor_muro, origen=(ancho_piso,0,0), rotacion_z=90, material='Muro_Pintura_Gris')

# Mobiliario planta alta
cama_principal = A.crear_cama('Cama_Principal', ancho=1.6, largo=2.0, origen=(1.2, 2.5, 0), material_colchon='Textil_Blanco', material_base='Madera_Nogal')
cama_secundaria = A.crear_cama('Cama_Secundaria', ancho=1.0, largo=2.0, origen=(ancho_piso-1.0-0.1, 2.5, 0), material_colchon='Textil_Blanco', material_base='Madera_Nogal')
baño = A.crear_bano('Bano', ancho=2.5, fondo=2.5, origen=(ancho_piso-2.5-0.1, 0.1, 0), material_piso='Porcelanato', material_muro='Muro_Pintura_Gris')

# --- Losa intermedia y escalera ---
losa_intermedia = A.crear_losa_rectangular('Losa_Intermedia', ancho=ancho_piso, fondo=fondo_piso, espesor=0.2, origen=(0,0,alto_piso), material='Hormigon')
hueco_escalera = A.abrir_vanos_batch_rectangulares(losa_intermedia, centros_world=[(ancho_piso/2, fondo_piso/2, alto_piso + 0.1)], ancho=1.1, alto=1.8)
escalera = A.crear_escalera_recta('Escalera', huella=0.28, contrahuella=0.18, ancho=1.1, num_peldanos=15, origen=(0,0,alto_piso), material='Madera_Roble')

# --- Iluminación y cámara ---
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(-10, -10, 15), energia=2.5)
A.crear_camara('Camara', ubicacion=(10, -10, 8), rotacion=(70, 0, 0))