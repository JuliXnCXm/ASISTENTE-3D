import blender_arch as A

A.limpiar_escena()

# --- Parámetros ---
ancho = 9.0
fondo = 7.0
alto = 2.7
grosor_muro = 0.15

# --- Materiales ---
mat_muro_int = "Muro_Pintura"
mat_suelo = "Parquet"
mat_bano = "Ceramica_Piso"
mat_cocina = "Porcelanato"
mat_madera = "Madera_Nogal"
mat_marco = "Marco_Blanco"

# --- Estructura y Muros Exteriores ---
piso_general = A.crear_piso("Piso_General", ancho, fondo, 0.02, origen=(ancho/2, fondo/2, 0))
A.asignar_material(piso_general, mat_suelo)

muro_frente = A.crear_muro("Muro_Frente", ancho, alto, grosor_muro, origen=(ancho/2, grosor_muro/2, 0))
muro_fondo = A.crear_muro("Muro_Fondo", ancho, alto, grosor_muro, origen=(ancho/2, fondo-grosor_muro/2, 0))
muro_izq = A.crear_muro("Muro_Izq", fondo, alto, grosor_muro, origen=(grosor_muro/2, fondo/2, 0), rotacion_z=90)
muro_der = A.crear_muro("Muro_Der", fondo, alto, grosor_muro, origen=(ancho-grosor_muro/2, fondo/2, 0), rotacion_z=90)
for m in [muro_frente, muro_fondo, muro_izq, muro_der]: A.asignar_material(m, mat_muro_int)

# --- Muros Interiores ---
# Cocina
muro_cocina = A.crear_muro("Muro_Cocina", 3.5, alto, grosor_muro, origen=(ancho-3.5-grosor_muro/2, 3.5/2, 0), rotacion_z=90)

# Pasillo y Dormitorio
muro_pasillo = A.crear_muro("Muro_Pasillo", 4.0, alto, grosor_muro, origen=(2.0, fondo-3.0-grosor_muro/2, 0))
muro_bano = A.crear_muro("Muro_Bano", 3.0, alto, grosor_muro, origen=(4.0, fondo-3.0/2, 0), rotacion_z=90)
for m in [muro_cocina, muro_pasillo, muro_bano]: A.asignar_material(m, mat_muro_int)

# --- Mobiliario ---
# Sala-Comedor
sofa = A.crear_sofa("Sofa", ancho=2.2, fondo=0.9, origen=(2.5, 1.0, 0), material="Tela_Beige")
mesa_comedor = A.crear_mesa("Mesa_Comedor", ancho=1.4, fondo=0.8, origen=(ancho-2.0, 2.0, 0), material_tablero=mat_madera)
for i in range(2): 
    A.crear_silla(f"Silla_A_{i}", origen=(ancho-2.4, 2.0 + i*0.8 - 0.4, 0), material=mat_madera)
    A.crear_silla(f"Silla_B_{i}", origen=(ancho-1.6, 2.0 + i*0.8 - 0.4, 0), material=mat_madera)

# Cocina
barra_cocina = A.crear_mesa("Barra_Cocina", ancho=1.5, fondo=0.6, alto=1.1, origen=(ancho-3.5-0.3, 2.5, 0))
mesada_cocina = A.crear_mesa("Mesada_Cocina", ancho=3.5, fondo=0.6, alto=0.9, origen=(ancho-0.3, 3.5/2, 0), material_tablero=mat_cocina)
mesada_cocina.rotation_euler[2] = 1.5708 # 90 degrees

# Dormitorio
cama = A.crear_cama("Cama_Doble", ancho=1.6, largo=2.0, origen=(2.0, fondo-1.5, 0), material_base=mat_madera)
armario = A.crear_armario("Armario", ancho=2.5, alto=2.4, fondo=0.6, origen=(1.35, fondo-2.8, 0))

# --- Puertas y Ventanas ---
puerta_entrada = A.crear_puerta("Puerta_Entrada", 0.9, 2.1, origen=(0.6, grosor_muro/2, 0))
A.abrir_vanos_batch_rectangulares(muro_frente, [(0.6, grosor_muro/2, 1.05)], 0.9, 2.1)

puerta_bano = A.crear_puerta("Puerta_Bano", 0.8, 2.1, origen=(4.0-0.5, fondo-3.0, 0))
A.abrir_vanos_batch_rectangulares(muro_pasillo, [(4.0-0.5, fondo-3.0-grosor_muro/2, 1.05)], 0.8, 2.1)

puerta_dorm = A.crear_puerta("Puerta_Dorm", 0.8, 2.1, origen=(0.5, fondo-3.0, 0))
A.abrir_vanos_batch_rectangulares(muro_pasillo, [(0.5, fondo-3.0-grosor_muro/2, 1.05)], 0.8, 2.1)

ventana_sala = A.crear_ventana("Ventana_Sala", 2.0, 1.5, origen=(ancho-2.5, grosor_muro/2, 0.9), material_marco=mat_marco)
A.abrir_vanos_batch_rectangulares(muro_frente, [(ancho-2.5, grosor_muro/2, 0.9+1.5/2)], 2.0, 1.5)

ventana_dorm = A.crear_ventana("Ventana_Dorm", 1.8, 1.5, origen=(grosor_muro/2, fondo-1.5, 0.9), material_marco=mat_marco)
ventana_dorm.rotation_euler[2] = 1.5708
A.abrir_vanos_batch_rectangulares(muro_izq, [(grosor_muro/2, fondo-1.5, 0.9+1.5/2)], 1.8, 1.5)

# --- Iluminación y Cámara ---
A.agregar_luz("Luz_Principal", ubicacion=(ancho/2, fondo/2, alto+1), energia=1000, tipo="AREA")
A.crear_camara("Camara", ubicacion=(5, -6, 6), rotacion=(60, 0, 30), activa=True)