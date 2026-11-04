import blender_arch as A

A.limpiar_escena()

# --- Materiales ---
mat_estuco = "Estuco"
mat_madera = "Madera_Roble"
mat_vidrio = "Vidrio_Templado"
mat_marco = "Marco_Aluminio"

# --- Planta Baja (Z=0) ---
muro_pb = A.crear_muro("Muro_PB", largo=10, alto=3.2, grosor=0.3, origen=(0, 0, 0), material=mat_estuco)
puerta_entrada = A.crear_puerta("Puerta_Entrada", ancho=2.0, alto=2.4, prof_marco=0.3, origen=(3.5, -0.15, 0), material_panel=mat_vidrio, material_marco=mat_marco)
ventana_pb = A.crear_ventana("Ventana_PB", ancho=2.5, alto=1.2, prof_marco=0.3, origen=(7.5, -0.15, 1.6), material_marco=mat_marco)

# --- Planta Alta (Z=3.2) ---
muro_pa = A.crear_muro("Muro_PA", largo=10, alto=3.2, grosor=0.3, origen=(0, 0.5, 3.2), material=mat_estuco)
cubierta = A.crear_techo_plano("Cubierta", ancho=10.3, fondo=0.6, espesor=0.2, origen=(-0.15, -0.15, 6.4), material=mat_estuco)

# --- Celosía de Lamas Verticales ---
num_lamas = 25
separacion = 0.15
for i in range(num_lamas):
    x_pos = i * separacion + separacion / 2
    z_pos = 3.2 + 0.15 # Altura superior de la lama
    lama = A.crear_muro(f"Lama_{i}", largo=10.3, alto=0.2, grosor=0.08, origen=(x_pos, 0, z_pos), material=mat_madera)
    A.asignar_material(lama, base_color=(0.4, 0.2, 0.1, 1))

# --- Entorno ---
A.crear_terreno_plano("Suelo", ancho=20, fondo=20, origen=(0, 0, -0.1), material="Cesped")
A.agregar_luz("Luz_Sol", tipo="SUN", ubicacion=(5, -10, 8), energia=3.0)