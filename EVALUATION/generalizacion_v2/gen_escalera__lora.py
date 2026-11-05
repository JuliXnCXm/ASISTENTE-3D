import blender_arch as A

A.limpiar_escena()

A.crear_escalera_recta(
    nombre="Escalera_Principal",
    huella=0.28,
    contrahuella=0.175,
    ancho=1.1,
    num_peldanos=14,
    con_contrahuellas=True,
    con_zancas=False,
    origen=(0, 0, 0),
    material="Madera"
)

piso_superior = A.crear_piso("Piso_Superior", ancho=3.0, fondo=4.0, espesor=0.05, origen=(0, 0, 2.8), material="Parquet")
piso_superior.location.z += 2.8

piso_inferior = A.crear_piso("Piso_Inferior", ancho=3.0, fondo=4.0, espesor=0.05, origen=(0, 0, -2.8), material="Parquet")
piso_inferior.location.z -= 2.8