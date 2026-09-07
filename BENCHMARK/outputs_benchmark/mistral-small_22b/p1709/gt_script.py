import blender_arch as A

A.limpiar_escena()

# Losa elevada 0.3m sobre el suelo
origen_losa = (0, 0, 0.3)
espesor_losa = 0.2
A.crear_losa_rectangular(nombre="PisoTerraza", ancho=6.0, fondo=4.0, espesor=espesor_losa, origen=origen_losa, material="Concreto_Piso")

# La baranda se coloca sobre el borde trasero de la losa
# Origen Z = origen_losa.z + espesor_losa
origen_baranda = (0, 4.0, origen_losa[2] + espesor_losa)
A.crear_baranda_lineal(nombre="Baranda", largo=6.0, altura=1.0, origen=origen_baranda, material="Acero_Inox")