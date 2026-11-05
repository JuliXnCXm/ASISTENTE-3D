import blender_arch as A
A.limpiar_escena()

# --- Parámetros ---
ancho_piso = 9.0
fondo_piso = 10.0
alto_piso = 2.8

# --- Materiales ---
mat_muro = "Muro_Pintura"
mat_suelo = "Parquet"
mat_losa = "Hormigon"
mat_madera = "Madera_Roble"

# --- Plantas ---
piso_baja = A.crear_piso("Piso_Baja", ancho=ancho_piso, fondo=fondo_piso, espesor=0.02, origen=(0,0,-0.01), material=mat_suelo)
piso_alta = A.crear_piso("Piso_Alta", ancho=ancho_piso, fondo=fondo_piso, espesor=0.02, origen=(0,0,-0.01), material=mat_suelo)

# --- Losa intermedia con hueco para escalera ---
losa_intermedia = A.crear_losa_rectangular("Losa_Intermedia", ancho=ancho_piso, fondo=fondo_piso, espesor=0.2, origen=(0,0,0), material=mat_losa)
hueco_escalera = A.abrir_vanos_batch_rectangulares(losa_intermedia, centros_world=[(ancho_piso/2, fondo_piso/2, 0.1)], ancho=1.2, alto=1.8)
escalera = A.crear_escalera_rectangular("Escalera", huella=0.28, contrahuella=0.175, ancho=1.2, num_peldanos=16, origen=(ancho_piso/2, fondo_piso/2, 0), material="Madera")

# --- Muros divisorios ---
muro_div1 = A.crear_muro("Muro_Div1", largo=ancho_piso, alto=alto_piso, grosor=0.15, origen=(0, fondo_piso-0.15, 0), material=mat_muro)
muro_div2 = A.crear_muro("Muro_Div2", largo=ancho_piso, alto=alto_piso, grosor=0.15, origen=(0, 0, 0), rotacion_z=-90, material=mat_muro)
muro_div3 = A.crear_muro("Muro_Div3", largo=ancho_piso, alto=alto_piso, grosor=0.15, origen=(ancho_piso-0.15, 0, 0), rotacion_z=90, material=mat_muro)
muro_div4 = A.crear_muro("Muro_Div4", largo=ancho_piso, alto=alto_piso, grosor=0.15, origen=(0, 0, 0), rotacion_z=90, material=mat_muro)

# --- Mobiliario planta baja ---
sofa = A.crear_sofa("Sofa", ancho=2.5, fondo=0.9, origen=(ancho_piso/2, 2.0, 0))
mesa_comedor = A.crear_mesa("Mesa_Comedor", ancho=1.8, fondo=0.9, origen=(ancho_piso/2, 5.0, 0))
armario = A.crear_armario("Armario", ancho=2.0, alto=2.4, fondo=0.6, origen=(ancho_piso/2, 0.1, 0))

# --- Mobiliario planta alta ---
cama1 = A.crear_cama("Cama_Principal", ancho=1.6, largo=2.0, origen=(ancho_piso/2, 2.0, alto_piso))
cama2 = A.crear_cama("Cama_Secundaria", ancho=1.4, largo=2.0, origen=(ancho_piso/2, 0.1, alto_piso))
baño = A.crear_bano("Bano", ancho=2.5, fondo=2.0, alto=2.8, origen=(ancho_piso/2, 7.5, alto_piso), material_piso=mat_suelo, material_muro=mat_muro)