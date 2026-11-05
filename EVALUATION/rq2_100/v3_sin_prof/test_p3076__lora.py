import blender_arch as A
A.limpiar_escena()

# --- ESTRUCTURA Y MUEBLES COMUNES ---
ancho_total = 8.0
fondo_total = 9.0
alto_piso = 2.8

# Crear el espacio principal
hab = A.crear_habitacion(
    nombre="Apartamento",
    ancho=ancho_total,
    fondo=fondo_total,
    alto=alto_piso,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Zona de entrada y circulación
A.crear_pared("Pared_Fondo", largo=ancho_total, alto=alto_piso, origen=(0, fondo_total-1.0, 0), rotacion_z=180)
A.crear_pared("Pared_Izq", largo=fondo_total, alto=alto_piso, origen=(0, 0, 0), rotacion_z=90)
A.crear_pared("Pared_Der", largo=fondo_total, alto=alto_piso, origen=(ancho_total, 0, 0), rotacion_z=-90)
A.crear_pared("Pared_Frente", largo=ancho_total, alto=alto_piso, origen=(0, 0, 0), rotacion_z=0)

# Mobiliario común
sofa = A.crear_sofa("Sofa_Principal", ancho=2.5, fondo=0.9, origen=(1.5, 1.5, 0))
sofa.rotation_euler[2] = 1.5708 # 90 grados
A.asignar_material(sofa, "Tela_Beige")

tv = A.crear_tv("TV", ancho=1.2, alto=0.6, fondo=0.2, origen=(ancho_total/2, 0.2, 0))
tv.rotation_euler[2] = 1.5708 # 90 grados
A.asignar_material(tv, "Marco_Negro")

# --- ZONA PRIVADA ---
# Pasillo distribuidor
pasillo = A.crear_habitacion(nombre="Pasillo", ancho=1.5, fondo=0.9, alto=alto_piso, origen=(ancho_total-1.5, 0, 0), material_muro="Muro_Pintura_Gris", material_suelo="Parquet")

# Dormitorio Principal
dorm_princ = A.crear_habitacion(nombre="Dormitorio_Principal", ancho=4.0, fondo=5.0, alto=alto_piso, origen=(0, 0, 0), material_muro="Muro_Pintura_Gris", material_suelo="Parquet")
dorm_princ.crear_ventana("Ventana_Esquina", ancho=2.0, alto=1.5, prof_marco=0.2, origen=(0.2, 0.2, 1.0), material_marco="Marco_Blanco", material_vidrio="Vidrio")
dorm_princ.crear_ventana("Ventana_Derecha", ancho=2.0, alto=1.5, prof_marco=0.2, origen=(2.0, 0.2, 1.0), material_marco="Marco_Blanco", material_vidrio="Vidrio")
dorm_princ.crear_puerta("Puerta_Bano", ancho=0.8, alto=2.1, origen=(0.2, 5.0, 0), material_panel="Madera_Roble", material_marco="Marco_Blanco")

# Baño en suite
baño_princ = A.crear_habitacion(nombre="Bano_Principal", ancho=2.5, fondo=2.5, alto=alto_piso, origen=(2.0, 5.0, 0), material_muro="Muro_Pintura_Gris", material_suelo="Porcelanato")
baño_princ.crear_puerta("Puerta_Ducha", ancho=0.8, alto=2.1, origen=(0.2, 0.2, 0), material_panel="Acero_Inox", material_marco="Acero_Inox")
baño_princ.crear_piso("Piso_Bano", ancho=2.5, fondo=2.5, origen=(0.2, 0.2, 0))

# Dormitorio Secundario
dorm_sec = A.crear_habitacion(nombre="Dormitorio_Secundario", ancho=3.0, fondo=4.0, alto=alto_piso, origen=(0, 5.0, 0), material_muro="Muro_Pintura_Gris", material_suelo="Parquet")

# --- ZONA CUCINA ---
# Cocina en L
cocina_largo = 4.0
cocina_ancho = 2.5
cocina_fondo = 2.0
cocina_prof = 0.6
cocina_origen = (ancho_total - cocina_largo, 0.5, 0)

# Encimera larga
encimera_larga = A.crear_mesa("Encimera_Larga", ancho=cocina_largo, fondo=cocina_fondo, alto=0.9, origen=(cocina_origen[0], cocina_origen[1]+cocina_fondo, cocina_origen[2]), material_tablero="Porcelanato")
encimera_larga.rotation_euler[2] = 1.5708 # 90 grados

# Encimera corta
encimera_corta = A.crear_mesa("Encimera_Corta", ancho=cocina_ancho, fondo=cocina_prof, alto=0.9, origen=(cocina_origen[0]+cocina_largo-cocina_ancho, cocina_origen[1], cocina_origen[2]), material_tablero="Porcelanato")
encimera_corta.rotation_euler[2] = 1.5708 # 90 grados

# Mobiliario cocina
cama_cocina = A.crear_armario("Cama_Cocina", ancho=cocina_ancho, alto=cocina_fondo, fondo=cocina_prof, origen=(cocina_origen[0]+cocina_largo-cocina_ancho, cocina_origen[1]-cocina_prof, cocina_origen[2]), material_panel="MDF_Blanco", material_marco="Marco_Negro")
cama_cocina.rotation_euler[2] = 1.5708 # 90 grados

# --- ILUMINACION Y CAMARA ---
A.agregar_luz("Luz_Principal", tipo="AREA", ubicacion=(ancho_total/2, fondo_total/2, alto_piso+1.5), energia=800)
A.crear_camara("Camara", ubicacion=(-5, -5, 5), rotacion=(70, 0, -45), activa=True)