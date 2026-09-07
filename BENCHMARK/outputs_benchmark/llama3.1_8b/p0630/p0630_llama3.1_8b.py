import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades del sofá
sofa_length = 2.5  # metros
sofa_width = 1.0   # metros
sofa_height = 0.8  # metros

# Crea el cuerpo del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -1.5, 0))
sofa_body = bpy.context.active_object
sofa_body.name = "Sofa Body"

# Agrega la tapicería al sofá
bpy.ops.mesh.primitive_plane_add(size=sofa_width, location=(0, -1.5, sofa_height))
sofa_seat = bpy.context.active_object
sofa_seat.name = "Sofa Seat"
sofa_seat.scale = (sofa_length, sofa_width, 0.2)
sofa_seat.location = (0, -1.5, sofa_height + 0.4)

# Agrega los respaldos al sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -1.5, sofa_height))
sofa_back = bpy.context.active_object
sofa_back.name = "Sofa Back"
sofa_back.scale = (sofa_length, 0.2, sofa_width)
sofa_back.location = (0, -1.5, sofa_height + 0.4)

# Define las propiedades de la mesa de centro
table_length = 1.5  # metros
table_width = 0.8   # metros
table_height = 0.6  # metros

# Crea la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=table_length, location=(0, -2.5, table_height))
table_body = bpy.context.active_object
table_body.name = "Table Body"

# Agrega los pies a la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=table_width, location=(-table_length/2, -2.5, 0))
table_leg1 = bpy.context.active_object
table_leg1.name = "Table Leg 1"
table_leg1.scale = (table_width, table_height, table_width)
table_leg1.location = (-table_length/2, -2.5, 0)

bpy.ops.mesh.primitive_cube_add(size=table_width, location=(table_length/2, -2.5, 0))
table_leg2 = bpy.context.active_object
table_leg2.name = "Table Leg 2"
table_leg2.scale = (table_width, table_height, table_width)
table_leg2.location = (table_length/2, -2.5, 0)

# Agrega la superficie a la mesa de centro
bpy.ops.mesh.primitive_plane_add(size=table_length, location=(0, -2.5, table_height))
table_surface = bpy.context.active_object
table_surface.name = "Table Surface"
table_surface.scale = (table_length, table_width, 0.1)
table_surface.location = (0, -2.5, table_height + 0.3)

# Aplica la tapicería al sofá y a la mesa de centro
sofa_seat.active_material = bpy.data.materials['Tela Gris']
table_surface.active_material = bpy.data.materials['Madera de Nogal']

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])