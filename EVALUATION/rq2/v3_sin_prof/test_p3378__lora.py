import blender_arch as A
A.limpiar_escena()

# --- Parámetros de la planta baja ---
ancho_pb = 7.0
fondo_pb = 12.0
alto_pb = 2.8
grosor_muro = 0.2

# --- Parámetros de la planta alta ---
ancho_pa = 7.0
fondo_pa = 12.0
alto_pa = 2.8
grosor_losa = 0.2

# --- Materiales ---
mat_muro = "Muro_Pintura"
mat_suelo_pb = "Parquet"
mat_suelo_pa = "Porcelanato"
mat_madera = "Madera_Roble"

# --- Crear la planta baja ---
A.crear_habitacion("Sala_Estar", ancho=ancho_pb, fondo=fondo_pb, alto=alto_pb, grosor_muro=grosor_muro, origen=(0, 0, 0), material_muro=mat_muro, material_suelo=mat_suelo_pb)
A.crear_habitacion("Comedor", ancho=ancho_pb, fondo=fondo_pb, alto=alto_pb, grosor_muro=grosor_muro, origen=(0, 0, 0), material_muro=mat_muro, material_suelo=mat_suelo_pb)
A.crear_habitacion("Cocina", ancho=ancho_pb, fondo=fondo_pb, alto=alto_pb, grosor_muro=grosor_muro, origen=(0, 0, 0), material_muro=mat_muro, material_suelo=mat_suelo_pb)
A.crear_habitacion("Aseo", ancho=2.0, fondo=1.5, alto=alto_pb, grosor_muro=grosor_muro, origen=(0, 0, 0), material_muro=mat_muro, material_suelo=mat_suelo_pb)

# --- Losa intermedia y hueco para escalera ---
losa_intermedia = A.crear_losa_rectangular("Losa_Intermedia", ancho=ancho_pb, fondo=fondo_pb, espesor=0.2, origen=(0, 0, alto_pb), material=mat_muro)
hueco_escalera = A.abrir_vanos_batch_rectangulares(losa_intermedia, centros_world=[(ancho_pb/2, fondo_pb/2, alto_pb + 0.1)], ancho=1.2, alto=1.9)
escalera = A.crear_escalera_rectangular("Escalera_Duplex", huella=0.28, contrahuella=0.18, ancho=1.2, num_peldanos=15, origen=(ancho_pb/2, fondo_pb/2, alto_pb), material="Madera")

# --- Materiales de la planta alta ---
mat_muro_pa = "Muro_Pintura_Gris"
mat_suelo_pa = "Porcelanato"

# --- Crear la planta alta ---
A.crear_habitacion("Dormitorio_Principal", ancho=ancho_pa, fondo=fondo_pa, alto=alto_pa, grosor_muro=grosor_muro, origen=(0, 0, alto_pb + grosor_losa), material_muro=mat_muro_pa, material_suelo=mat_suelo_pa)
A.crear_habitacion("Dormitorio_Secundario", ancho=ancho_pa, fondo=fondo_pa, alto=alto_pa, grosor_muro=grosor_muro, origen=(0, 0, alto_pb + grosor_losa), material_muro=mat_muro_pa, material_suelo=mat_suelo_pa)
A.crear_habitacion("Baño_Compartido", ancho=2.0, fondo=1.5, alto=alto_pa, grosor_muro=grosor_muro, origen=(0, 0, alto_pb + grosor_losa), material_muro=mat_muro_pa, material_suelo=mat_suelo_pa)