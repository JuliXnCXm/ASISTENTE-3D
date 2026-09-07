import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del edificio
ancho = 15
alto = 10
profundidad = 20

# Crea el cuerpo principal del edificio
bpy.ops.mesh.primitive_cube_add(size=alto, location=(0, 0, -5))
cuerpo_principal = bpy.context.active_object
cuerpo_principal.scale = (ancho, alto, profundidad)

# Crea la fachada del edificio
fachada = cuerpo_principal.modifiers.new('Fachada', 'ARRAY').offset = (ancho / 2, 0, 0)
bpy.ops.object.modifier_apply(modifier='Fachada')

# Crea las ventanas de la fachada
ventana_ancho = ancho / 10
ventana_alto = alto / 5

for i in range(10):
    for j in range(3):
        x = (i * ancho) + (j * ventana_ancho)
        y = -alto / 2 + (j * ventana_alto)
        bpy.ops.mesh.primitive_cube_add(size=ventana_alto, location=(x, y, 0))
        ventana = bpy.context.active_object
        ventana.scale = (ventana_ancho, ventana_alto, ventana_alto)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])