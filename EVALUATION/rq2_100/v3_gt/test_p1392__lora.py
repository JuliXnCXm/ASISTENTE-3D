import blender_arch as A

A.limpiar_escena()

# Muro base de la fachada
muro_fachada = A.crear_muro(
    nombre="Muro_Fachada",
    largo=10.0,
    alto=6.0,
    grosor=0.3,
    material="Ladrillo_Rojo"
)

# Crear ventanas en una retícula
ancho_ventana = 1.5
alto_ventana = 1.2
num_filas = 2
num_columnas = 4

for fila in range(num_filas):
    for col in range(num_columnas):
        # Calcular posición de cada ventana
        x_pos = -5 + (col * (ancho_ventana + 0.1)) + (ancho_ventana / 2)
        z_pos = 2.5 + (fila * (alto_ventana + 0.1)) + (alto_ventana / 2)
        
        # Crear la ventana en esa posición
        A.crear_ventana(
            nombre=f"Ventana_{fila}_{col}",
            ancho=ancho_ventana,
            alto=alto_ventana,
            prof_marco=0.1,
            origen=(x_pos, -0.15, z_pos),
            material_marco="Marco_Aluminio",
            material_vidrio="Vidrio"
        )