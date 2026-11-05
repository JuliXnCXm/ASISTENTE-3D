import blender_arch as A
A.limpiar_escena()
A.crear_mesa(nombre='Isla_Cocina', ancho=2.0, fondo=1.0, alto=0.9, origen=(0, 0, 0), material_tablero='Cuarzo')
A.extruir_con_huecos(nombre='Fregadero_Impreso', contorno=[(-0.2, -0.1), (0.2, -0.1), (0.2, 0.1), (-0.2, 0.1)], agujeros=[[0, 0]], altura=-0.05, material='Acero_Inox').location = (0, 0, 0.9)
A.agregar_luz(nombre='Luz_Isla_1', tipo='SPOT', ubicacion=(-1.5, -1.5, 3.0), energia=800)
A.agregar_luz(nombre='Luz_Isla_2', tipo='SPOT', ubicacion=(0, -1.5, 3.0), energia=800)
A.agregar_luz(nombre='Luz_Isla_3', tipo='SPOT', ubicacion=(1.5, -1.5, 3.0), energia=800)