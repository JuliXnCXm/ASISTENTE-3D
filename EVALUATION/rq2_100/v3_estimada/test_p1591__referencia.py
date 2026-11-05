import blender_arch as A

A.limpiar_escena()

# Plaza peatonal
A.crear_terreno_plano(
    'Plaza', 
    ancho=20.0, 
    fondo=30.0, 
    espesor=0.2, 
    origen=(0,-15,0), 
    material='Concreto_Piso'
)

# Edificio
A.crear_edificio_n_pisos(
    nombre='OficinasCentrales',
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=2.2,
    ventana_alfeizar=0.5,
    ventana_separacion=2.5,
    origen=(0, 0, 0),
    material_fachada='Estuco',
    material_marco='Marco_Aluminio',
    material_vidrio='Vidrio'
)

# Iluminación exterior
A.agregar_luz('Sol', tipo='SUN', ubicacion=(-20, -20, 30), energia=3.0)