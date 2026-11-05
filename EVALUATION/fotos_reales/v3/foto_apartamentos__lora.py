import blender_arch as A

A.limpiar_escena()

# --- Parámetros del edificio ---
ancho_edificio = 12.0
alto_edificio = 3.5
num_pisos = 4
grosor_muro = 0.3
grosor_losa = 0.3
voladizo_losa = 0.5

# --- Crear losas de piso y muros ---
for i in range(num_pisos + 1):
    z_piso = i * alto_edificio
    A.crear_losa_rectangular(f"Plaza_{i}", ancho=ancho_edificio, fondo=10, espesor=grosor_losa, origen=(0, -5, z_piso), material="Concreto_Piso")
    for j in range(4):
        x_muro = j * (ancho_edificio / 3)
        A.crear_muro(f"Muro_Frontal_{i}_{j}", largo=ancho_edificio, alto=alto_edificio, grosor=grosor_muro, origen=(x_muro, -5, z_piso), material="Muro_Pintura")

# --- Crear ventanas y balcones ---
for i in range(num_pisos):
    for j in range(3):
        x_vano = j * (ancho_edificio / 3) + ancho_edificio/6
        y_vano = -5 + grosor_muro/2
        z_vano = (i+1) * alto_edificio
        A.abrir_vanos_batch_rectangulares(f"Muro_Frontal_{i}_0", centros_world=[(x_vano, y_vano, z_vano)], ancho=1.5, alto=1.2)
        A.crear_ventana(f"Ventana_Frontal_{i}_{j}", ancho=1.5, alto=1.2, prof_marco=grosor_muro, origen=(x_vano, y_vano, z_vano), material_marco="Marco_Blanco", material_vidrio="Vidrio")
        A.crear_losa_rectangular(f"Balcon_Frontal_{i}_{j}", ancho=1.5, fondo=0.9, espesor=0.25, origen=(x_vano, y_vano - 0.45, z_vano + 1.2), material="Madera_Roble")

# --- Crear puertas y mobiliario ---
A.crear_puerta("Puerta_Acceso", ancho=2.0, alto=2.2, prof_marco=grosor_muro, origen=(-1.0, -5, 0), material_panel="Madera_Nogal", material_marco="Marco_Negro")
A.crear_puerta("Puerta_Vehicular", ancho=4.0, alto=2.2, prof_marco=grosor_muro, origen=(1.0, -5, 0), material_panel="Acero_Inox", material_marco="Marco_Negro")

A.crear_mesa("Mesa_Exterior", ancho=1.5, fondo=0.75, alto=0.75, origen=(0, -6, 0), material_tablero="Madera_Roble")
A.crear_silla("Silla_Exterior_1", origen=(0, -6.5, 0), material="Madera_Roble")
A.crear_silla("Silla_Exterior_2", origen=(0, -5.5, 0), material="Madera_Roble")

# --- Crear tejado ---
A.crear_tejado_plano("Tejado", ancho=ancho_edificio, fondo=10, espesor=0.2, origen=(0, -5, num_pisos * alto_edificio), material="Teja")