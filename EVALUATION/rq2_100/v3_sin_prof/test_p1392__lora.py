import blender_arch as A

A.limpiar_escena()

# Crear la fachada base
fachada = A.crear_muro(
    nombre="Fachada_Ladrillo",
    largo=10.0,
    alto=6.0,
    grosor=0.3,
    material="Ladrillo_Rojo"
)

# Definir parámetros de la retícula y las ventanas
ancho_fachada = 10.0
alto_fachada = 6.0
num_huecos_x = 4
num_huecos_y = 2
ancho_ventana = 1.5
alto_ventana = 1.2
grosor_marco = 0.1

# Calcular dimensiones y posiciones
ancho_modulo = ancho_ventana + grosor_marco
alto_modulo = alto_ventana + grosor_marco
num_modulos_x = int(ancho_fachada / ancho_modulo)
num_modulos_y = num_huecos_y

# Crear ventanas y abrir huecos
for i in range(num_huecos_x):
    for j in range(num_huecos_y):
        x_pos = i * ancho_modulo
        z_pos = j * alto_modulo
        
        # Crear la ventana en su lugar
        A.crear_ventana(
            nombre=f"Ventana_{i}_{j}",
            ancho=ancho_ventana,
            alto=alto_ventana,
            prof_marco=grosor_marco,
            origen=(x_pos, 0, z_pos),
            material_marco="Marco_Aluminio",
            material_vidrio="Vidrio"
        )
        
        # Abrir el hueco en la fachada
        A.abrir_vanos_batch_rectangulares(
            muro=fachada,
            centros_world=[(x_pos + ancho_ventana/2, 0, z_pos + alto_ventana/2)],
            ancho=ancho_ventana,
            alto=alto_ventana
        )