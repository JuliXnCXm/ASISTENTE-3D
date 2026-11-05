import blender_arch as A

A.limpiar_escena()

terreno = A.crear_terreno_plano(
    nombre='Cesped_Piscina',
    ancho=20.0, 
    fondo=20.0,
    espesor=0.2,
    origen=(10, 10, -1.7),
    material='Cesped'
)

ancho_borde = 1.5
ancho_piscina = 8.0
fondo_piscina = 4.0
ancho_total = ancho_piscina + 2 * ancho_borde
fondo_total = fondo_piscina + 2 * ancho_borde

contorno_borde = [
    (0, 0), (ancho_total, 0), 
    (ancho_total, fondo_total), (0, fondo_total)
]
agujero_piscina = [
    [(ancho_borde, ancho_borde), (ancho_borde + ancho_piscina, ancho_borde), 
     (ancho_borde + ancho_piscina, ancho_borde + fondo_piscina), (ancho_borde, ancho_borde + fondo_piscina)]
]

borde = A.extruir_con_huecos(
    nombre='Borde_Piscina',
    contorno=contorno_borde,
    agujeros=agujero_piscina,
    altura=0.2,
    material='Concreto_Piso',
)
borde.location = (10 - ancho_total/2, 10 - fondo_total/2, -0.2)

agua = A.crear_losa_rectangular(
    nombre='Agua_Piscina',
    ancho=ancho_piscina,
    fondo=fondo_piscina,
    espesor=1.5, # Profundidad
    origen=(10, 10, -1.7),
    material='Agua'
)