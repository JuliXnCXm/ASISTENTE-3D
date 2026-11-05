import blender_arch as A
A.limpiar_escena()
hab = A.crear_habitacion(nombre='Cocina', ancho=4.0, fondo=3.0, alto=2.8, grosor_muro=0.15, origen=(0, 0, 0), material_muro='Ladrillo_Rojo')
meson_largo = 2.5
meson_ancho = 1.0
meson_alto = 0.9
meson_origen = (-meson_largo / 2, -meson_ancho / 2, 0)
A.crear_mesa(nombre='Meson_Largo', ancho=meson_largo, fondo=meson_ancho, alto=meson_alto, origen=meson_origen, material_tablero='MDF_Blanco')
meson_curvo = 1.5
meson_curvo_alto = 0.9
meson_curvo_origen = (0, -meson_curvo / 2, 0)
A.crear_mesa(nombre='Meson_Curvo', ancho=meson_curvo, fondo=meson_curvo, alto=meson_curvo_alto, origen=meson_curvo_origen, material_tablero='MDF_Blanco')
mesa_central = A.crear_mesa(nombre='Mesa_Central', ancho=1.2, fondo=0.7, alto=0.75, origen=(0, 0, 0), material_tablero='Madera_Roble')
silla1 = A.crear_silla(nombre='Silla_1', origen=(-0.6, 0.6, 0), material='Madera')
silla2 = A.crear_silla(nombre='Silla_2', origen=(0.6, 0.6, 0), material='Madera')
silla3 = A.crear_silla(nombre='Silla_3', origen=(0.6, -0.6, 0), material='Madera')
silla4 = A.crear_silla(nombre='Silla_4', origen=(-0.6, -0.6, 0), material='Madera')
ancho_ventana = 1.5
alto_ventana = 1.2
centro_ventana_z = 1.2
A.abrir_vanos_grid_local(hab['Muro_Trasero'], filas=1, cols=1, x0=0, y0=-1.5, z0=centro_ventana_z, dx=4.0, dy=0, dz=0, ancho=ancho_ventana, alto=alto_ventana, profundidad=0.0, nombre='Ventana_Cocina')