import blender_arch as A

A.limpiar_escena()

# --- Parámetros ---
ancho_edificio = 10.0
alto_piso = 3.2
num_pisos = 2
grosor_muro = 0.3
retranqueo = 0.5
ancho_losa_cubierta = 10.0

# --- Materiales ---
mat_estuco = "Estuco"
mat_marco = "Marco_Negro"
mat_vidrio = "Vidrio_Templado"
mat_madera = "Madera_Roble"
mat_techo = "Hormigon"

# --- Estructura base ---
muro_p1 = A.crear_muro("Muro_P1", largo=ancho_edificio, alto=alto_piso, grosor=grosor_muro, origen=(0, 0, 0), material=mat_estuco)
muro_p2 = A.crear_muro("Muro_P2", largo=ancho_edificio, alto=alto_piso, grosor=grosor_muro, origen=(0, 0, alto_piso), material=mat_estuco)

# --- Entrada principal (planta baja) ---
ventana_entrada = A.crear_ventana("Ventana_Entrada", ancho=2.0, alto=2.2, prof_marco=grosor_muro, divisiones=(1,1), origen=(-1.0, -0.1, 0), material_marco=mat_marco, material_vidrio=mat_vidrio)
A.abrir_vanos_batch_rectangulares(muro_p1, centros_world=[(-1.0, -0.1, 1.1)], ancho=2.0, alto=2.2)

# --- Planta alta (retranqueada) ---
muro_p3 = A.crear_muro("Muro_P3", largo=ancho_edificio, alto=alto_piso, grosor=grosor_muro, origen=(0, retranqueo, alto_piso), material=mat_estuco)
muro_p4 = A.crear_muro("Muro_P4", largo=ancho_edificio, alto=alto_piso, grosor=grosor_muro, origen=(0, retranqueo, alto_piso), material=mat_estuco)

# --- Cubierta y celosía ---
losa_cubierta = A.crear_losa_rectangular("Losa_Cubierta", ancho=ancho_losa_cubierta, fondo=ancho_edificio, espesor=0.2, origen=(0, 0, alto_piso + grosor_muro), material=mat_techo)
celosia = A.crear_celosia_vertical("Celosia_Solar", ancho=ancho_edificio, alto=alto_piso, num_lamas=16, origen=(0, retranqueo, alto_piso + grosor_muro), material=mat_madera)

# --- Vano para ventanal superior ---
ancho_ventanal = 4.0
alto_ventanal = 2.2
centro_ventanal = (0, 0, alto_piso + grosor_muro + alto_ventanal / 2)
A.abrir_vanos_batch_rectangulares(muro_p3, centros_world=[centro_ventanal], ancho=ancho_ventanal, alto=alto_ventanal)

# --- Iluminación y cámara ---
A.agregar_luz("Luz_Principal", tipo="SUN", ubicacion=(5, -5, 10), energia=2.5)
A.crear_camara("Camara_Fachada", ubicacion=(0, -12, 5), rotacion=(80, 0, 0))