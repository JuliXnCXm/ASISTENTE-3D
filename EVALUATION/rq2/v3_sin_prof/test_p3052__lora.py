import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA Y ZONAS ---
ancho_total = 7.0
fondo_total = 8.0
alto_piso = 2.8
grosor_muro = 0.2

# Muros perimetrales
muro_frente = A.crear_muro('Muro_Frente', largo=ancho_total, alto=alto_piso, grosor=grosor_muro, origen=(0,0,0), material='Muro_Pintura')
muro_fondo = A.crear_muro('Muro_Fondo', largo=ancho_total, alto=alto_piso, grosor=grosor_muro, origen=(0,fondo_total,0), material='Muro_Pintura')
muro_izq = A.crear_muro('Muro_Izq', largo=fondo_total, alto=alto_piso, grosor=grosor_muro, origen=(0,0,0), rotacion_z=90, material='Muro_Pintura')
muro_der = A.crear_muro('Muro_Der', largo=fondo_total, alto=alto_piso, grosor=grosor_muro, origen=(ancho_total,0,0), rotacion_z=90, material='Muro_Pintura')

# Suelo y Techo
suelo = A.crear_piso('Suelo', ancho=ancho_total, fondo=fondo_total, espesor=0.05, origen=(0,0,0), material='Parquet')
techo = A.crear_techo_plano('Techo', ancho=ancho_total, fondo=fondo_total, espesor=0.2, origen=(0,0,alto_piso), material='Yeso')

# --- MOBILIARIO ZONA DE DÍA (SALA-COMEDOR) ---
# Sala
sofa = A.crear_sofa('Sofa', ancho=2.2, fondo=0.9, origen=(1.4, 1.5, 0), material='Tela_Gris')
mesa_comedor = A.crear_mesa('Mesa_Comedor', ancho=1.6, fondo=0.8, alto=0.75, origen=(2.5, 2.5, 0), material_tablero='Madera_Roble')
# Comedor
silla_1 = A.crear_silla('Silla_1', origen=(2.5, 1.5, 0), material='Madera_Roble')
silla_2 = A.crear_silla('Silla_2', origen=(3.5, 1.5, 0), material='Madera_Roble')
silla_3 = A.crear_silla('Silla_3', origen=(4.5, 1.5, 0), material='Madera_Roble')
silla_4 = A.crear_silla('Silla_4', origen=(2.5, 2.5, 0), material='Madera_Roble')
silla_5 = A.crear_silla('Silla_5', origen=(3.5, 2.5, 0), material='Madera_Roble')
silla_6 = A.crear_silla('Silla_6', origen=(4.5, 2.5, 0), material='Madera_Roble')

# --- MOBILIARIO BAÑO ---
baño = A.crear_habitacion('Baño', ancho=2.0, fondo=2.5, alto=2.8, grosor_muro=grosor_muro, origen=(ancho_total - 2.0, 0, 0), material_muro='Porcelanato', material_suelo='Ceramica_Piso', material_techo='Yeso')
baño.agregar_objeto('Bañera', ancho=1.5, fondo=0.7, origen=(0.2, 0.2, 0), material='Porcelanato')
baño.agregar_objeto('Toallero', ancho=0.2, fondo=0.2, origen=(0.2, 1.8, 0), material='Acero_Inox')
baño.agregar_objeto('Espejo', ancho=1.5, fondo=0.2, origen=(0.2, 2.3, 1.8), material='Vidrio')

# --- MOBILIARIO DORMITORIO ---
dormitorio = A.crear_habitacion('Dormitorio', ancho=3.0, fondo=4.0, alto=2.8, grosor_muro=grosor_muro, origen=(0, fondo_total - 4.0, 0), material_muro='Muro_Pintura', material_suelo='Parquet', material_techo='Yeso')
dormitorio.agregar_objeto('Cama', ancho=1.6, largo=2.0, origen=(0.7, 1.0, 0), material_base='Madera_Nogal', material_colchon='Textil_Blanco')
dormitorio.agregar_objeto('Armario', ancho=1.8, fondo=0.6, origen=(1.1, 0.2, 0), material='MDF_Blanco')

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('Luz_Sala', tipo='AREA', ubicacion=(ancho_total/2, 1.5, alto_piso + 2.0), energia=200)
A.crear_camara('Camara', ubicacion=(ancho_total/2, -5, alto_piso/2), rotacion=(75, 0, 0))