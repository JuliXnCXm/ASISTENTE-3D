import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA Y ZONAS FUNCIONALES ---
ancho_total = 7.0
fondo_total = 8.0
alto_piso = 2.8
grosor_muro = 0.15

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
sofa = A.crear_sofa('Sofa', ancho=2.4, fondo=0.9, origen=(1.3, 0.6, 0), material='Tela_Gris')
mesa_comedor = A.crear_mesa('Mesa_Comedor', ancho=1.8, fondo=0.9, alto=0.75, origen=(2.5, 2.5, 0), material_tablero='Madera_Roble')
silla_1 = A.crear_silla('Silla_1', origen=(2.5, 1.5, 0), material='Cuero')
silla_2 = A.crear_silla('Silla_2', origen=(3.5, 1.5, 0), material='Cuero')
silla_3 = A.crear_silla('Silla_3', origen=(2.5, 3.5, 0), material='Cuero')

# Comedor
silla_4 = A.crear_silla('Silla_4', origen=(4.5, 2.5, 0), material='Cuero')
silla_5 = A.crear_silla('Silla_5', origen=(5.5, 2.5, 0), material='Cuero')

# --- MOBILIARIO ZONA CUCINA ---
encimera_cocina = A.crear_mesa('Encimera_Cocina', ancho=2.0, fondo=0.6, alto=0.9, origen=(0.5, 5.5, 0), material_tablero='Acero_Inox')
armario_cocina = A.crear_armario('Armario_Cocina', ancho=2.0, alto=2.4, fondo=0.6, origen=(0.5, 4.5, 0), material_cuerpo='MDF_Blanco')

# --- MOBILIARIO BAÑO ---
bañera = A.crear_bañera('Bañera', ancho=1.5, fondo=0.7, origen=(5.5, 0.5, 0), material='Porcelanato')
lavabo = A.crear_mesa('Lavabo', ancho=0.6, fondo=0.4, alto=0.85, origen=(0.5, 6.5, 0), material_tablero='Mármol')
toallero = A.crear_toallero('Toallero', origen=(0.5, 7.0, 0), material='Acero_Inox')

# --- MOBILIARIO DORMITORIO ---
cama = A.crear_cama('Cama_Principal', ancho=1.6, largo=2.0, origen=(1.2, 6.5, 0), material_colchon='Textil_Blanco', material_base='Madera_Nogal')
armario_dormitorio = A.crear_armario('Armario_Dormitorio', ancho=1.8, alto=2.4, fondo=0.6, origen=(1.2, 4.5, 0), material_cuerpo='MDF_Blanco')

# --- ILUMINACIÓN Y CAMARA ---
A.agregar_luz('Luz_Sala', tipo='AREA', ubicacion=(3.5, 1.5, 2.5), energia=200)
A.agregar_luz('Luz_Cocina', tipo='AREA', ubicacion=(0.5, 5.5, 2.5), energia=150)
A.agregar_luz('Luz_Bano', tipo='AREA', ubicacion=(5.5, 0.5, 2.5), energia=150)
A.agregar_luz('Luz_Dormitorio', tipo='AREA', ubicacion=(1.2, 6.5, 2.5), energia=150)

A.crear_camara('Camara_Vivienda', ubicacion=(3.5, -3, 1.5), rotacion=(70, 0, 0))