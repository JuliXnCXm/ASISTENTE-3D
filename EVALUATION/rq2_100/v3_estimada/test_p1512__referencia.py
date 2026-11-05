import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)

# Crear el edificio
A.crear_edificio_n_pisos(
    nombre="Bloque_Residencial",
    pisos=5,
    ancho=20.0,
    fondo=12.0,
    alto_piso=3.0,
    con_columnas=True,
    modulo_columna_x=5.0,
    modulo_columna_y=6.0,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.2,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    material_fachada="Hormigon",
    material_losa="Hormigon",
    material_vidrio="Vidrio",
    material_marco="Marco_Negro"
)

# Añadir iluminación solar
A.agregar_luz(
    nombre="Luz_Solar",
    tipo="SUN",
    ubicacion=(-15, -20, 30),
    energia=2.5
)