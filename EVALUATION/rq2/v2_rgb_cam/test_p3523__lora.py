import blender_arch as A

A.limpiar_escena()

# --- Materiales ---
mat_muro = "Hormigon"
mat_losa = "Concreto_Piso"
mat_vidrio = "Vidrio_Templado"
mat_marco = "Marco_Negro"

# --- Parámetros ---
ancho_fachada = 10.0
alto_piso = 2.8
num_pisos = 2
retranqueo = 1.0

# --- Crear Losa de la Planta Baja ---
A.crear_losa_rectangular(
    nombre="Losa_PB",
    ancho=ancho_fachada,
    fondo=10.0,
    espesor=0.2,
    origen=(0, 0, 0),
    material=mat_losa
)

# --- Muro de la Planta Baja ---
muro_pb = A.crear_muro(
    nombre="Muro_PB",
    largo=ancho_fachada,
    alto=alto_piso,
    grosor=0.3,
    origen=(0, 0, 0),
    material=mat_muro
)

# --- Cubierta Plana Transitable ---
cubierta = A.crear_techo_plano(
    nombre="Cubierta",
    ancho=ancho_fachada,
    fondo=10.0,
    espesor=0.2,
    origen=(0, 0, alto_piso + 0.2),
    material=mat_losa
)

# --- Muro de la Planta Alta ---
muro_pa = A.crear_muro(
    nombre="Muro_PA",
    largo=ancho_fachada,
    alto=alto_piso,
    grosor=0.3,
    origen=(0, retranqueo, alto_piso),
    material=mat_muro
)

# --- Ventanal de la Planta Alta ---
ventanal_pa = A.crear_ventana(
    nombre="Ventanal_PA",
    ancho=ancho_fachada - 0.6,
    alto=alto_piso,
    prof_marco=0.3,
    divisiones=(3, 1),
    origen=(0.3, retranqueo, alto_piso),
    material_marco=mat_marco,
    material_vidrio=mat_vidrio
)
A.abrir_vanos_batch_rectangulares(muro_pa, centros_world=[(ancho_fachada / 2, retranqueo, alto_piso + 0.15)], ancho=ancho_fachada - 0.6, alto=alto_piso)

# --- Iluminación y Cámara ---
A.agregar_luz("Luz_Sol", tipo="SUN", ubicacion=(-5, -5, 10), energia=2.5)
A.crear_camara("Camara_Fachada", ubicacion=(ancho_fachada/2, -10, alto_piso*1.5), rotacion=(70, 0, 0))