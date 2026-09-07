import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del edificio
ancho = 15.0
pisos = 3
altura_piso = 3.0

# Crear los pisos
for piso in range(pisos):
    # Crear el piso como una caja
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura_piso * piso))
    piso_obj = bpy.context.object
    piso_obj.scale = (ancho, ancho, altura_piso)

# Crear las ventanas
ventana_ancho = 2.5
ventana_alto = 1.5

for x in range(int(ancho / ventana_ancho)):
    for y in range(int(ancho / ventana_alto)):
        for piso in range(pisos):
            # Posición de la ventana en el piso actual
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x * ventana_ancho - ancho/2 + ventana_ancho/2, y * ventana_alto - ancho/2 + ventana_alto/2, altura_piso * piso))
            ventana_obj = bpy.context.object
            ventana_obj.scale = (ventana_ancho, ventana_alto, 1)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)