import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la cocina en L
cocina_l = [
    ('muro', 'fondo', (6, 4, 0), (0, 0, 2.8)),
    ('muro', 'lado', (6, 4, 0), (0, 0, 2.8)),
    ('muro', 'largo', (6, 4, 0), (0, 0, 2.8)),
    ('muro', 'corto', (6, 4, 0), (0, 0, 2.8))
]

A.crear_muros(cocina_l)

# Módulos bajos y altos
modulos = [
    ('armario', 'bajo', (1.5, 0.6, 0), (0, 0, 0.85)),
    ('armario', 'alto', (1.5, 0.6, 0), (0, 0, 1.8)),
    ('encimera', 'base', (1.5, 0.6, 0.85), (0, 0, 0.02)),
    ('armario', 'bajo', (4.5, 0.6, 0), (0, 3.4, 0.85)),
    ('armario', 'alto', (4.5, 0.6, 0), (0, 3.4, 1.8)),
    ('encimera', 'base', (4.5, 0.6, 0.85), (0, 3.4, 0.02))
]
A.crear_armarios(modulos)

# Isla central
isla_base = A.crear_losa_rectangular('Isla_Base', 2.0, 1.0, 0.05, origen=(2.0, 1.5, 0.85))
isla_encimera = A.crear_losa_rectangular('Isla_Encimera', 2.0, 1.0, 0.02, origen=(2.0, 1.5, 0.87))

# Taburetes
taburete1 = A.crear_silla('Taburete_1', origen=(2.0, 0.5, 0.85))
taburete2 = A.crear_silla('Taburete_2', origen=(2.0, 2.5, 0.85))

# Iluminación y cámara
A.agregar_luz('Luz_Principal', tipo='AREA', ubicacion=(3, 2, 2.5), energia=250)
A.crear_camara('Camara_Cocina', ubicacion=(-3, -4, 3), rotacion=(70, 0, -45))