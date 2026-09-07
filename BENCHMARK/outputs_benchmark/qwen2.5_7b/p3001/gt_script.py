import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Definición de Parámetros ---
ancho_total = 6.0
profundidad_total = 8.5
alto_piso = 2.8
grosor_muro = 0.15
grosor_losa = 0.2

# --- Materiales ---
mat_muro_ext = "Ladrillo_Rojo"
mat_muro_int = "Muro_Pintura"
mat_suelo = "Parquet"
mat_techo = "Yeso"
mat_marco = "Marco_Blanco"
mat_madera = "Madera_Roble"

# --- Geometría Base ---
losa_suelo = A.crear_losa_rectangular("LosaSuelo", ancho_total, profundidad_total, grosor_losa, origen=(ancho_total/2, profundidad_total/2, -grosor_losa), material=mat_suelo)
A.asignar_material(losa_suelo, mat_suelo)

techo = A.crear_techo_plano("Techo", ancho_total, profundidad_total, espesor=grosor_losa, origen=(ancho_total/2, profundidad_total/2, alto_piso), material=mat_techo)

# --- Muros Exteriores ---
muro_frente = A.crear_muro("MuroFrente", ancho_total, alto_piso, grosor_muro, origen=(ancho_total/2, grosor_muro/2, 0), material=mat_muro_ext)
muro_fondo = A.crear_muro("MuroFondo", ancho_total, alto_piso, grosor_muro, origen=(ancho_total/2, profundidad_total - grosor_muro/2, 0), material=mat_muro_ext)
muro_izq = A.crear_muro("MuroIzq", profundidad_total, alto_piso, grosor_muro, origen=(grosor_muro/2, profundidad_total/2, 0), material=mat_muro_ext)
muro_der = A.crear_muro("MuroDer", profundidad_total, alto_piso, grosor_muro, origen=(ancho_total - grosor_muro/2, profundidad_total/2, 0), material=mat_muro_ext)

# --- Muros Interiores (Dormitorio y Baño) ---
# Dormitorio: 3.5m de ancho, 3.5m de fondo
# Baño: 2.2m de ancho, 2.0m de fondo
prof_dorm = 3.5
ancho_dorm = 3.5
ancho_bano = 2.2

muro_div_dorm = A.crear_muro("MuroDivDorm", ancho_dorm, alto_piso, grosor_muro, origen=(ancho_total - grosor_muro/2 - ancho_dorm/2, prof_dorm, 0), material=mat_muro_int)
muro_div_bano_dorm = A.crear_muro("MuroDivBanoDorm", prof_dorm, alto_piso, grosor_muro, origen=(ancho_total-ancho_dorm-grosor_muro, prof_dorm/2, 0), material=mat_muro_int)

# --- Vano y Puertas ---
A.abrir_vanos_batch_rectangulares(muro_frente, centros_world=[(2, grosor_muro/2, 1.5)], ancho=1.8, alto=2.0) # Ventana Sala
A.abrir_vanos_batch_rectangulares(muro_frente, centros_world=[(ancho_total - 1, grosor_muro/2, 1.1)], ancho=0.9, alto=2.1) # Puerta Principal
A.abrir_vanos_batch_rectangulares(muro_div_dorm, centros_world=[(ancho_total - ancho_dorm/2, prof_dorm - grosor_muro/2, 1.1)], ancho=0.8, alto=2.1) # Puerta Dorm
A.abrir_vanos_batch_rectangulares(muro_div_bano_dorm, centros_world=[(ancho_total - ancho_dorm - grosor_muro/2, 1.0, 1.1)], ancho=0.7, alto=2.1) # Puerta Baño
A.crear_puerta("PuertaPrincipal", 0.9, 2.1, prof_marco=grosor_muro, origen=(ancho_total - 1, 0, 0), material_panel=mat_madera, material_marco=mat_marco)
A.crear_puerta("PuertaDorm", 0.8, 2.1, prof_marco=grosor_muro, origen=(ancho_total - ancho_dorm/2, prof_dorm - grosor_muro, 0), material_panel=mat_madera, material_marco=mat_marco)
A.crear_puerta("PuertaBano", 0.7, 2.1, prof_marco=grosor_muro, origen=(ancho_total - ancho_dorm, 1.0, 0), material_panel=mat_madera, material_marco=mat_marco)
A.crear_ventana("VentanaSala", 1.8, 2.0, prof_marco=grosor_muro, origen=(2, 0, 0.5), material_marco=mat_marco)

# --- Mobiliario ---
# Sala-Comedor-Cocina
A.crear_sofa("Sofa", ancho=2.0, origen=(2.0, profundidad_total - 1.2, 0))
A.crear_mesa("MesaComedor", ancho=1.2, fondo=0.7, alto=0.75, origen=(1.5, 2.5, 0))
A.crear_silla("Silla1", origen=(1.5, 2.1, 0))
A.crear_silla("Silla2", origen=(1.5, 2.9, 0))
A.crear_mesa("MesadaCocina", ancho=0.6, fondo=2.5, alto=0.9, origen=(0.3 + grosor_muro, profundidad_total - 1.25 - grosor_muro, 0))

# Dormitorio
A.crear_cama("CamaPrincipal", ancho=1.5, largo=2.0, origen=(ancho_total - ancho_dorm/2 - grosor_muro, 1.2, 0))
A.crear_armario("ArmarioDorm", ancho=1.8, alto=2.4, fondo=0.6, origen=(ancho_total - 1.1, prof_dorm - 0.6 - grosor_muro, 0))

# --- Iluminación y Cámara ---
A.agregar_luz("LuzCenital", tipo="AREA", ubicacion=(ancho_total/2, profundidad_total/2, alto_piso - 0.1), energia=800)
A.crear_camara("CamaraPrincipal", ubicacion=(-4, 12, 6), rotacion=(65, 0, -20))