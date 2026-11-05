import blender_arch as A

A.limpiar_escena()

# Terreno base
A.crear_terreno_plano(
    nombre="Terreno_Cesped",
    ancho=12,
    fondo=10,
    espesor=0.2,
    origen=(0, 0, -0.1),
    material="Cesped"
)

# Borde de la piscina
A.crear_losa_rectangular(
    nombre="Borde_Piscina",
    ancho=8 + 1.5 * 2,
    fondo=4 + 1.5 * 2,
    espesor=0.2,
    origen=(-1.5, -1.5, 0),
    material="Concreto_Piso"
)

# Agua de la piscina
A.extruir_con_huecos(
    nombre="Agua_Piscina",
    contorno=[(-4, -2), (4, -2), (4, 2), (-4, 2)],
    agujeros=[[(-3, -1.5), (3, -1.5), (3, 1.5), (-3, 1.5)]],
    altura=1.5,
    material="Agua"
)