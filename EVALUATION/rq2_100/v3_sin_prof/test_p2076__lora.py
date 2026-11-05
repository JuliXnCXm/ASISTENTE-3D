import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
A.crear_habitacion(
    nombre="Sala_Estar",
    ancho=6.0,
    fondo=4.5,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar un sofá contra la pared del fondo
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.5,
    origen=(1.75, 0.2, 0),
    material="Tela_Beige"
)

# Colocar una alfombra en el suelo
alfombra = A.crear_alfombra(
    nombre="Alfombra_Sala",
    ancho=3.0,
    fondo=2.0,
    origen=(1.5, 1.5, 0),
    material="Textil_Blanco"
)

# Crear y posicionar estanterías modulares
def crear_estanteria_modular(nombre, ancho_total, num_estantes):
    ancho_por_estante = ancho_total / num_estantes
    espesor_panel = 0.04
    alto_panel = 0.35
    
    for i in range(num_estantes):
        x_pos = i * ancho_por_estante
        z_pos = alto_panel * (i + 1)
        
        # Paneles verticales
        bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0.1, z_pos))
        panel = bpy.context.active_object
        panel.name = f"Panel_{i+1}"
        panel.dimensions = (espesor_panel, 0.2, alto_panel)
        A.asignar_material(panel, "Madera_Roble")
        
        # Paneles horizontales
        bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0.1, z_pos + alto_panel/2))
        panel = bpy.context.active_object
        panel.name = f"Panel_Horiz_{i+1}"
        panel.dimensions = (ancho_por_estante, 0.02, alto_panel)
        A.asignar_material(panel, "Madera_Roble")

# Estantería de 3 estantes
estanteria = crear_estanteria_modular("Estanteria_Diseño", 1.8, 3)
estanteria.location = (0.1, 0.1, 0.9)