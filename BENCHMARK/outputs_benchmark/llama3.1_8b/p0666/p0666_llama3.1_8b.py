import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las proporciones del sofá
sofa_length = 2.5  # metros
sofa_width = 1.0   # metros
sofa_height = 0.8  # metros

# Crea el cuerpo del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, sofa_height))
sofa_body = bpy.context.active_object
sofa_body.name = 'Sofa Body'

# Crea las patas del sofá
pata_length = 0.5  # metros
bpy.ops.mesh.primitive_cube_add(size=pata_length, location=(sofa_length/2, -sofa_width/2, sofa_height))
pata1 = bpy.context.active_object
pata1.name = 'Sofa Pata 1'
pata1.location = (0, -sofa_width/2, sofa_height + pata_length)

bpy.ops.mesh.primitive_cube_add(size=pata_length, location=(sofa_length/2, -sofa_width/2, sofa_height))
pata2 = bpy.context.active_object
pata2.name = 'Sofa Pata 2'
pata2.location = (0, -sofa_width/2 + pata_length, sofa_height)

bpy.ops.mesh.primitive_cube_add(size=pata_length, location=(-sofa_length/2, -sofa_width/2, sofa_height))
pata3 = bpy.context.active_object
pata3.name = 'Sofa Pata 3'
pata3.location = (0, -sofa_width/2, sofa_height + pata_length)

bpy.ops.mesh.primitive_cube_add(size=pata_length, location=(-sofa_length/2, -sofa_width/2, sofa_height))
pata4 = bpy.context.active_object
pata4.name = 'Sofa Pata 4'
pata4.location = (0, -sofa_width/2 + pata_length, sofa_height)

# Crea la tapicería del sofá
tapiceria_thickness = 0.1  # metros
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, sofa_height))
tapiceria = bpy.context.active_object
tapiceria.name = 'Sofa Tapiceria'
tapiceria.location = (0, -sofa_width/2, sofa_height + tapiceria_thickness)

# Define las proporciones de la mesa de centro
mesa_length = 1.5  # metros
mesa_width = 0.8   # metros
mesa_height = 0.7  # metros

# Crea el cuerpo de la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=mesa_length, location=(0, -mesa_width/2, mesa_height))
mesa_body = bpy.context.active_object
mesa_body.name = 'Mesa Body'

# Aplica una textura gris a la tapicería del sofá y al cuerpo de la mesa de centro
bpy.data.materials.new('Gris')
mat_grey = bpy.data.materials['Gris']
mat_grey.diffuse_color = (0.5, 0.5, 0.5)

tapiceria.active_material = mat_grey
mesa_body.active_material = mat_grey

# Aplica una textura de madera a la mesa de centro
bpy.data.materials.new('Madera')
mat_wood = bpy.data.materials['Madera']
mat_wood.diffuse_color = (0.8, 0.6, 0.4)
mat_wood.specular_intensity = 0.5

mesa_body.active_material = mat_wood

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])