import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la fachada
ancho = 10
alto = 6
espesor_ladrillo = 0.1

# Crea el plano base de la fachada
bpy.ops.mesh.primitive_plane_add(size=ancho, location=(0, 0, -alto/2))

# Selecciona el plano y lo renombramos
objeto_base = bpy.context.active_object
objeto_base.name = "Fachada"

# Crea la geometría de los ladrillos
for i in range(int(ancho / espesor_ladrillo)):
    for j in range(int(alto / espesor_ladrillo)):
        # Calcula la posición del ladrillo actual
        x = (i + 0.5) * espesor_ladrillo - ancho/2
        y = (j + 0.5) * espesor_ladrillo - alto/2
        
        # Crea un nuevo objeto para el ladrillo
        bpy.ops.mesh.primitive_cube_add(size=espesor_ladrillo, location=(x, y, 0))
        
        # Selecciona el cubo y lo renombramos
        objeto_ladrillo = bpy.context.active_object
        objeto_ladrillo.name = f"Ladrillo_{i}_{j}"

# Crea la puerta de entrada
puerta_ancho = ancho / 5
puerta_alto = alto
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, 0, -alto/2 + (alto-puerta_alto)/2))
objeto_puerta = bpy.context.active_object
objeto_puerta.name = "Puerta"

# Crea las ventanas
ventana_ancho = ancho / 10
ventana_alto = alto / 5

for i in range(1, 3):
    # Calcula la posición de la ventana actual
    x = (i - 0.5) * ancho/2
    
    # Crea un nuevo objeto para la ventana
    bpy.ops.mesh.primitive_cube_add(size=ancho, location=(x, 0, -alto/2 + (alto-ventana_alto)/2))
    
    # Selecciona el cubo y lo renombramos
    objeto_ventana = bpy.context.active_object
    objeto_ventana.name = f"Ventana_{i}"

# Guarda la escena si se especificó un archivo de salida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])