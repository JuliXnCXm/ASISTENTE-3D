import blender_arch as A
A.limpiar_escena()

# --- ESTRUCTURA Y HORMIGON ---
piso = A.crear_piso('Piso', ancho=8, fondo=9, espesor=0.05, material='Concreto_Piso')
muro_fondo = A.crear_muro('Muro_Fondo', largo=8, alto=2.8, grosor=0.15, origen=(0, 9, 0.05), material='Muro_Pintura_Gris')
muro_izq = A.crear_muro('Muro_Izq', largo=9, alto=2.8, grosor=0.15, origen=(0, 0, 0.05), rotacion_z=-90, material='Muro_Pintura_Gris')
muro_der = A.crear_muro('Muro_Der', largo=9, alto=2.8, grosor=0.15, origen=(8, 0, 0.05), rotacion_z=90, material='Muro_Pintura_Gris')

# --- ZONA ABIERTA (SALA-COMEDOR) ---
sofa = A.crear_sofa('Sofa', ancho=2.5, fondo=0.9, origen=(1.5, 6, 0.05), material='Tela_Beige')
mesa_comedor = A.crear_mesa('Mesa_Comedor', ancho=1.8, fondo=0.9, alto=0.75, origen=(3.5, 1.5, 0.05), material_tablero='Madera_Roble')
cama_secundaria = A.crear_cama('Cama_Secundaria', ancho=1.4, largo=2.0, origen=(0.5, 1.5, 0.05), material_colchon='Textil_Blanco', material_base='Madera_Nogal')

# --- COCINA SEMIABIERTA (L) ---
cocina_muro1 = A.crear_muro('Muro_Cocina_1', largo=4, alto=2.8, grosor=0.1, origen=(4, 0, 0.05), rotacion_z=90, material='MDF_Blanco')
cocina_muro2 = A.crear_muro('Muro_Cocina_2', largo=5, alto=2.8, grosor=0.1, origen=(4, 0, 0.05), rotacion_z=0, material='MDF_Blanco')
cocina_mueble_sup = A.crear_panel_lineal('Mueble_Cocina_Sup', largo=4, alto=0.9, prof=0.3, origen=(4, 0, 2.5), material='MDF_Blanco')
cocina_mueble_inf = A.crear_panel_lineal('Mueble_Cocina_Inf', largo=4, alto=0.6, prof=0.3, origen=(4, 0, 0.9), material='MDF_Blanco')
cocina_encimera = A.crear_panel_lineal('Encimera_Cocina', largo=4, alto=0.02, prof=0.6, origen=(4, 0, 1.5), material='Porcelanato')

# --- PASILLO DISTRIBUIDOR ---
pasillo = A.crear_muro('Pasillo', largo=9, alto=2.8, grosor=0.1, origen=(8, 0, 0.05), rotacion_z=90, material='Muro_Pintura_Gris')

# --- ZONA PRIVADA (DORMITORIOS Y BAÑOS) ---
dormitorio_principal = A.crear_dormitorio('Dormitorio_Principal', ancho=3.0, largo=4.0, origen=(0, 4, 0.05), material_colchon='Textil_Blanco', material_base='Madera_Nogal')
baño_princ = A.crear_bano('Bano_Principal', ancho=2.5, fondo=2.5, origen=(0, 0, 0.05), material_piso='Porcelanato', material_muro='Muro_Pintura_Gris')

dormitorio_secundario = A.crear_dormitorio('Dormitorio_Secundario', ancho=2.0, largo=2.0, origen=(6, 4, 0.05), material_colchon='Textil_Blanco', material_base='Madera_Nogal')
baño_gen = A.crear_bano('Bano_General', ancho=2.5, fondo=2.5, origen=(6, 0, 0.05), material_piso='Porcelanato', material_muro='Muro_Pintura_Gris')