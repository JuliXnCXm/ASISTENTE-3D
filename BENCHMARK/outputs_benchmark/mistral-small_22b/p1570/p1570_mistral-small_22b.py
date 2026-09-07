import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el tejado a dos aguas
def create_roof():
    # Crear el plano base del tejado
    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 3))
    roof = bpy.context.object

    # Añadir modificador de bisagra para crear el tejado a dos aguas
    bpy.ops.object.modifier_add(type='BEND')
    bend_modifier = roof.modifiers['Bend']
    bend_modifier.angle = 1.5708  # Ángulo de 90 grados en radianes
    bend_modifier.axis = 'X'

# Crear el tejado a dos aguas
create_roof()

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as(filepath=os.environ['BLEND_OUT'])