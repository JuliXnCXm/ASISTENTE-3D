import blender_arch as A

A.limpiar_escena()

# Parámetros de la fachada
num_plantas = 5
ancho_modulo = 4.0
alto_planta = 3.0
grosor_muro = 0.3
ancho_balcon = 2.0
profundidad_balcon = 1.0
espesor_baranda = 0.05
ancho_puerta = 1.8
alto_puerta = 2.2

# Crear los muros principales de la fachada
for i in range(num_plantas):
    A.crear_muro(f"Muro_Fachada_{i+1}", largo=ancho_modulo * num_plantas, alto=alto_planta, grosor=grosor_muro, origen=(0, 0, i * alto_planta), material="Estuco")

# Crear balcones y barandillas
for i in range(num_plantas):
    for j in range(4):
        x_pos = j * ancho_modulo
        z_pos = i * alto_planta
        
        # Balcon
        A.crear_losa_rectangular(f"Balcon_{i+1}_{j+1}", ancho=ancho_balcon, fondo=profundidad_balcon, espesor=0.2, origen=(x_pos + ancho_modulo/2 - ancho_balcon/2, 0, z_pos + alto_planta/2 - 0.1), material="Hormigon")
        
        # Barandilla
        A.crear_baranda_lineal(f"Barandilla_{i+1}_{j+1}", largo=ancho_balcon, origen=(x_pos + ancho_modulo/2 - ancho_balcon/2, 0, z_pos + alto_planta + 0.2), material="Vidrio_Templado")

# Crear puertas correderas
for i in range(num_plantas):
    for j in range(4):
        x_pos = j * ancho_modulo
        z_pos = i * alto_planta
        
        A.abrir_vanos_batch_rectangulares(
            "Puerta_Corredera",
            centros_world=[(x_pos + ancho_modulo/2, 0, z_pos + alto_puerta/2)],
            ancho=ancho_puerta,
            alto=alto_puerta
        )
        A.crear_puerta(
            f"Puerta_Corredera_{i+1}_{j+1}",
            ancho=ancho_puerta,
            alto=alto_puerta,
            prof_marco=grosor_muro,
            origen=(x_pos + ancho_modulo/2 - ancho_puerta/2, 0, z_pos),
            material_panel="Vidrio_Templado",
            material_marco="Marco_Negro"
        )

# Cubierta plana
A.crear_techo_plano("Cubierta_Plan", ancho=ancho_modulo * num_plantas, fondo=profundidad_balcon + 1.0, espesor=0.2, origen=(0, 0, num_plantas * alto_planta), material="Hormigon")