import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros Generales ---
ancho = 6.0
fondo = 7.5
alto_piso = 2.8
grosor_muro = 0.15

# --- PLANTA BAJA (Z=0) ---
# Suelo PB
piso_pb = A.crear_losa_rectangular("Piso_PB", ancho, fondo, 0.2, origen=(ancho/2, fondo/2, 0))
A.asignar_material(piso_pb, nombre="Porcelanato")

# Muros perimetrales PB
muro_pbf = A.crear_muro("Muro_PBF", ancho, alto_piso, grosor_muro, origen=(0,0,0))
muro_pbt = A.crear_muro("Muro_PBT", ancho, alto_piso, grosor_muro, origen=(0,fondo,0))
muro_pbi = A.crear_muro("Muro_PBI", fondo, alto_piso, grosor_muro, origen=(0,0,0), rotacion_z=90)
muro_pbd = A.crear_muro("Muro_PBD", fondo, alto_piso, grosor_muro, origen=(ancho,0,0), rotacion_z=90)

# Muros interiores PB (Cocina y Aseo)
muro_cocina = A.crear_muro("Muro_Cocina", 3.0, alto_piso, grosor_muro, origen=(0, 3.5, 0))
muro_cocina_pasillo = A.crear_muro("Muro_Cocina_Pasillo", 3.5, alto_piso, grosor_muro, origen=(3.0, 0, 0), rotacion_z=90)
muro_aseo = A.crear_muro("Muro_Aseo", 2.0, alto_piso, grosor_muro, origen=(3.0, 3.5, 0), rotacion_z=90)

# Escalera
escalera = A.crear_escalera_recta("Escalera_Principal", num_peldanos=16, huella=0.28, contrahuella=0.175, ancho=1.0, origen=(4.8, 0.5, 0))

# Mobiliario PB
sofa = A.crear_sofa("Sofa", ancho=2.2, origen=(1.5, 6.2, 0))
mesa_comedor = A.crear_mesa("Mesa_Comedor", ancho=1.4, fondo=0.8, origen=(4.0, 5.5, 0))
for i in range(4):
    silla = A.crear_silla(f"Silla_{i}", origen=(3.5 + (i%2)*1.0, 5.2 + (i//2)*0.6, 0))

# --- PLANTA ALTA (Z=2.8) ---
# Losa PA con hueco para escalera
ancho_esc = 1.0
largo_esc = 16 * 0.28
contorno_losa = [(0,0), (ancho,0), (ancho,fondo), (0,fondo)]
hueco_esc = [
    (ancho-grosor_muro-ancho_esc, 0.5),
    (ancho-grosor_muro, 0.5),
    (ancho-grosor_muro, 0.5 + largo_esc),
    (ancho-grosor_muro-ancho_esc, 0.5 + largo_esc)
]
losa_pa = A.extruir_con_huecos("Losa_PA", contorno=contorno_losa, agujeros=[hueco_esc], altura=0.2, material="Hormigon")
losa_pa.location.z = alto_piso
piso_pa = A.crear_piso("Piso_PA", ancho, fondo, 0.02, origen=(ancho/2, fondo/2, alto_piso + 0.2))
A.asignar_material(piso_pa, nombre="Parquet")

# Muros perimetrales PA
muro_paf = A.crear_muro("Muro_PAF", ancho, alto_piso, grosor_muro, origen=(0,0,alto_piso))
muro_pat = A.crear_muro("Muro_PAT", ancho, alto_piso, grosor_muro, origen=(0,fondo,alto_piso))
muro_pai = A.crear_muro("Muro_PAI", fondo, alto_piso, grosor_muro, origen=(0,0,alto_piso), rotacion_z=90)
muro_pad = A.crear_muro("Muro_PAD", fondo, alto_piso, grosor_muro, origen=(ancho,0,alto_piso), rotacion_z=90)

# Muros interiores PA (Dormitorios y Baño)
muro_dorm_div = A.crear_muro("Muro_Dorm_Div", ancho, alto_piso, grosor_muro, origen=(0, 4.0, alto_piso))
muro_bano_dorm = A.crear_muro("Muro_Bano_Dorm", 4.0, alto_piso, grosor_muro, origen=(3.5, 0, alto_piso), rotacion_z=90)

# Mobiliario PA
cama_ppal = A.crear_cama("Cama_Ppal", ancho=1.6, largo=2.0, origen=(3.0, 6.3, alto_piso+0.2))
armario_ppal = A.crear_armario("Armario_Ppal", ancho=2.5, fondo=0.6, origen=(0.15, 4.2, alto_piso+0.2))
cama_sec = A.crear_cama("Cama_Sec", ancho=1.0, largo=2.0, origen=(1.75, 2.8, alto_piso+0.2), material_base="Madera")
cama_sec.rotation_euler[2] = 1.5708

# --- Configuración Final ---
A.crear_camara("Camara_Duplex", ubicacion=(10, -10, 8), rotacion=(65, 0, 45), activa=True)
A.agregar_luz("Luz_General", tipo="SUN", ubicacion=(5, -5, 10), energia=3.0)