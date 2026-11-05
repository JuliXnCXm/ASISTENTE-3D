import blender_arch as A
A.limpiar_escena()

# Crear la habitación base
hab = A.crear_habitacion(
    nombre="Salon",
    ancho=5.0,
    fondo=4.0,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Mueble de TV flotante
A.crear_mesa(
    nombre="Mueble_TV",
    ancho=2.0,
    fondo=0.4,
    alto=0.4,
    origen=(1.5, 3.6, 0),
    material_tablero="MDF_Blanco"
)

# Estantería de obra con booleanos
estanteria = A.crear_losa_rectangular("Estanteria", 2.0, 0.3, 0.2, origen=(1.5, 0.7, 0))
estanteria.rotation_euler[2] = 1.5708 # 90 grados

# Nicho izquierdo
A.extruir_con_huecos(
    "Nicho_Izq",
    contorno=[(0, 0), (0.2, 0), (0.2, 0.3), (0, 0.3)],
    agujeros=[[(0.05, 0.05), (0.15, 0.05), (0.15, 0.25), (0.05, 0.25)]],
    altura=0.2,
    material="Madera_Roble"
).location = (1.5, 0.7, 0)

# Nicho derecho
A.extruir_con_huecos(
    "Nicho_Der",
    contorno=[(2.0, 0), (2.0-0.2, 0), (2.0-0.2, 0.3), (2.0, 0.3)],
    agujeros=[[(1.95, 0.05), (1.85, 0.05), (1.85, 0.25), (1.95, 0.25)]],
    altura=0.2,
    material="Madera_Roble"
).location = (1.5, 0.7, 0)

# Sofá grande
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.5,
    fondo=0.9,
    origen=(1.25, 1.0, 0),
    material="Tela_Gris"
)