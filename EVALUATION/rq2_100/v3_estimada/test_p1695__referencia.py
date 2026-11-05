import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)

# Crear la plaza o terreno base
A.crear_terreno_plano(
    nombre="Plaza_Edificio",
    ancho=40.0,
    fondo=30.0,
    espesor=0.3,
    origen=(0, 0, -0.15),
    material="Concreto_Piso"
)

# Crear el edificio
A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(-10, -7.5, 0),
    material_fachada="Estuco",
    material_losa="Hormigon",
    material_vidrio="Vidrio",
    material_marco="Marco_Aluminio"
)

# Añadir iluminación
A.agregar_luz(
    nombre="Luz_Solar",
    tipo="SUN",
    ubicacion=(-15, -20, 25),
    energia=3.0
)

# Configurar cámara
A.crear_camara(
    nombre="Camara_Plaza",
    ubicacion=(30, -25, 15),
    rotacion=(75, 0, 45),
    activa=True
)