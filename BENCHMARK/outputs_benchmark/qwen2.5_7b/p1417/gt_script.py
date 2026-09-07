import blender_arch as A
A.limpiar_escena()
ancho = 4.0
fondo = 3.0
alto = 2.5
dim_col = 0.2
material_madera = "Madera_Roble"
# Columnas en las esquinas
A.crear_columna(nombre="Col_FI", seccion="rect", ancho=dim_col, fondo=dim_col, alto=alto, origen=(0, 0, 0), material=material_madera)
A.crear_columna(nombre="Col_FD", seccion="rect", ancho=dim_col, fondo=dim_col, alto=alto, origen=(ancho - dim_col, 0, 0), material=material_madera)
A.crear_columna(nombre="Col_TI", seccion="rect", ancho=dim_col, fondo=dim_col, alto=alto, origen=(0, fondo - dim_col, 0), material=material_madera)
A.crear_columna(nombre="Col_TD", seccion="rect", ancho=dim_col, fondo=dim_col, alto=alto, origen=(ancho - dim_col, fondo - dim_col, 0), material=material_madera)
# Techo ligero que cubre las columnas
A.crear_techo_plano(nombre="Techo_Pergola", ancho=ancho, fondo=fondo, espesor=0.15, origen=(0, 0, alto), material=material_madera)