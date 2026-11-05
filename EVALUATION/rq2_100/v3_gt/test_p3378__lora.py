import blender_arch as A
A.limpiar_escena()

# --- Parámetros ---
ancho_piso = 9.0
fondo_piso = 10.0
alto_piso = 2.8
grosor_muro = 0.2

# --- Estructura y mobiliario planta baja ---
losa_p1 = A.crear_losa_rectangular('Losa_P1', ancho=ancho_piso, fondo=fondo_piso, espesor=0.2, origen=(0,0,-0.2), material='Hormigon')
muro_frente_pb = A.crear_muro('Muro_Frente_PB', largo=ancho_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,0,0), material='Muro_Pintura_Gris')
muro_fondo_pb = A.crear_muro('Muro_Fondo_PB', largo=ancho_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,fondo_piso,0), material='Muro_Pintura_Gris')
muro_izq_pb = A.crear_muro('Muro_Izq_PB', largo=fondo_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,0,0), rotacion_z=-90, material='Muro_Pintura_Gris')
muro_der_pb = A.crear_muro('Muro_Der_PB', largo=fondo_piso, alto=alto_piso, grosor=grosor_muro, origen=(ancho_piso,0,0), rotacion_z=90, material='Muro_Pintura_Gris')

# --- Mobiliario planta baja ---
sofa_pb = A.crear_sofa('Sofa_PB', ancho=2.5, fondo=0.9, origen=(1.75, 1.5, 0), material='Tela_Gris')
mesa_comedor_pb = A.crear_mesa('Mesa_Comedor_PB', ancho=1.8, fondo=0.9, origen=(3.5, 2.5, 0), material_tablero='Madera_Nogal')
armario_pb = A.crear_armario('Armario_PB', ancho=1.5, alto=2.4, fondo=0.6, origen=(ancho_piso-1.5-0.1, 0.3, 0), material_cuerpo='MDF_Blanco')

# --- Estructura y mobiliario planta alta ---
losa_p2 = A.crear_losa_rectangular('Losa_P2', ancho=ancho_piso, fondo=fondo_piso, espesor=0.2, origen=(0,0,alto_piso+0.2), material='Hormigon')
muro_frente_pa = A.crear_muro('Muro_Frente_PA', largo=ancho_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,0,alto_piso), material='Muro_Pintura_Gris')
muro_fondo_pa = A.crear_muro('Muro_Fondo_PA', largo=ancho_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,fondo_piso,alto_piso), material='Muro_Pintura_Gris')
muro_izq_pa = A.crear_muro('Muro_Izq_PA', largo=fondo_piso, alto=alto_piso, grosor=grosor_muro, origen=(0,0,alto_piso), rotacion_z=-90, material='Muro_Pintura_Gris')
muro_der_pa = A.crear_muro('Muro_Der_PA', largo=fondo_piso, alto=alto_piso, grosor=grosor_muro, origen=(ancho_piso,0,alto_piso), rotacion_z=90, material='Muro_Pintura_Gris')

# --- Mobiliario planta alta ---
cama_principal = A.crear_cama('Cama_Principal', ancho=1.6, largo=2.0, origen=(ancho_piso/2, fondo_piso-2.0-0.1, alto_piso), material_colchon='Textil_Blanco', material_base='Madera_Roble')
cama_secundaria = A.crear_cama('Cama_Secundaria', ancho=1.0, largo=1.9, origen=(ancho_piso/2, 0.1, alto_piso), material_colchon='Textil_Blanco', material_base='Madera_Roble')
baño_pa = A.crear_bano('Bano_PA', ancho=2.5, fondo=2.5, alto=2.8, origen=(ancho_piso-2.5-0.1, fondo_piso-2.5-0.1, alto_piso), material_piso='Porcelanato')

# --- Escalera ---
escalera = A.crear_escalera_rectangular('Escalera', huella=0.28, contrahuella=0.18, ancho=1.1, num_peldanos=12, origen=(0, 0, 0), material='Madera_Roble')
escalera.rotation_euler[2] = 1.5708 # 90 grados

# --- Iluminación y cámara ---
A.agregar_luz('Luz_Principal', tipo='AREA', ubicacion=(ancho_piso/2, fondo_piso/2, alto_piso*0.9), energia=250)
A.crear_camara('Camara', ubicacion=(-10, -10, 10), rotacion=(70, 0, -45), activa=True)