import blender_arch as A

A.limpiar_escena()

# --- Parámetros ---
ancho_edificio = 10.0
alto_piso = 3.2
grosor_muro = 0.3
retranqueo = 0.5
ancho_losa_cubierta = 10.0

# --- Materiales ---
mat_estuco = "Estuco"
mat_marco = "Marco_Negro"
mat_vidrio = "Vidrio_Templado"
mat_madera = "Madera_Roble"
mat_hormigon = "Hormigon"

# --- Planta Baja ---
muro_pb = A.crear_muro("Muro_PB", largo=ancho_edificio, alto=alto_piso, grosor=grosor_muro, origen=(0, 0, 0), material=mat_estuco)
ventana_pb = A.crear_ventana("Ventana_PB", ancho=3.0, alto=2.8, prof_marco=grosor_muro, divisiones=(1,1), origen=(3.5, 0, 0), material_marco=mat_marco, material_vidrio=mat_vidrio)

# --- Planta Alta ---
muro_pa = A.crear_muro("Muro_PA", largo=ancho_edificio, alto=alto_piso, grosor=grosor_muro, origen=(0, retranqueo, alto_piso), material=mat_estuco)
ventana_pa = A.crear_ventana("Ventana_PA", ancho=6.0, alto=2.8, prof_marco=grosor_muro, divisiones=(3,1), origen=(2.0, retranqueo, alto_piso), material_marco=mat_marco, material_vidrio=mat_vidrio)

# --- Cubierta ---
losa_cubierta = A.crear_techo_plano("Losa_Cubierta", ancho=ancho_losa_cubierta, fondo=ancho_edificio, espesor=0.2, origen=(0, 0, alto_piso*2), material=mat_hormigon)

# --- Celosía de Lamas Verticales ---
num_lamas = 12
separacion_lamas = 0.1
for i in range(num_lamas):
    x_pos = -ancho_edificio/2 + (i * (ancho_edificio / (num_lamas-1)) + separacion_lamas/2)
    lama = A.crear_panel_vertical(f"Lama_{i}", ancho=0.05, alto=alto_piso, prof=0.1, origen=(x_pos, 0, alto_piso), material=mat_madera)
    A.asignar_material(lama, base_color=(0.7, 0.7, 0.7, 1))

# --- Iluminación y Cámara ---
A.agregar_luz("Luz_Sol", tipo="SUN", ubicacion=(-5, -10, 10), energia=5)
A.crear_camara("Camara", ubicacion=(0, -15, 5), rotacion=(80, 0, 0), activa=True)