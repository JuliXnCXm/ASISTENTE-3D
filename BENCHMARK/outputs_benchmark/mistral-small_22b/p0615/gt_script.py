import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Dimensiones del espacio
ancho_total = 8.0
fondo_total = 6.0
alto_piso = 3.0
grosor_muro = 0.2

# Crear el contenedor de la habitación
A.crear_habitacion(
    nombre="Espacio_Abierto",
    ancho=ancho_total,
    fondo=fondo_total,
    alto=alto_piso,
    grosor_muro=grosor_muro,
    material_muro="Muro_Pintura",
    material_suelo="Porcelanato",
    material_techo="Yeso"
)

# --- Zona de Estar ---
A.crear_sofa(
    nombre="Sofa_Estar",
    ancho=2.5, fondo=0.9, alto_asiento=0.45,
    origen=(grosor_muro + 0.2, 1.5, 0),
    material="Tela_Beige"
)
A.crear_estanteria(
    nombre="Estanteria_Libros",
    ancho=1.5, alto=2.4, fondo=0.3,
    origen=(ancho_total - 1.5 - grosor_muro, grosor_muro + 0.1, 0),
    material="MDF_Blanco"
)

# --- Zona de Comedor ---
A.crear_mesa(
    nombre="Mesa_Comedor",
    ancho=1.8, fondo=0.9, alto=0.76,
    origen=(ancho_total / 2, fondo_total - 2.0, 0),
    material_tablero="Madera_Nogal"
)
A.crear_silla(nombre="Silla_1", origen=(ancho_total / 2 - 0.5, fondo_total - 2.8, 0), material="Madera_Nogal")
A.crear_silla(nombre="Silla_2", origen=(ancho_total / 2 + 0.5, fondo_total - 2.8, 0), material="Madera_Nogal")
A.crear_silla(nombre="Silla_3", origen=(ancho_total / 2 - 0.5, fondo_total - 1.2, 0), material="Madera_Nogal")
A.crear_silla(nombre="Silla_4", origen=(ancho_total / 2 + 0.5, fondo_total - 1.2, 0), material="Madera_Nogal")

# --- Iluminación ---
A.agregar_luz(
    nombre="Luz_Principal",
    tipo="AREA",
    ubicacion=(ancho_total / 2, fondo_total / 2, alto_piso - 0.1),
    energia=800
)