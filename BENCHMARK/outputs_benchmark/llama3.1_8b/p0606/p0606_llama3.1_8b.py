import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades del objeto
mat_wood = bpy.data.materials.new(name="Madera de Roble")
mat_wood.diffuse_color = (0.5, 0.2, 0.1)
mat_wood.specular_intensity = 0.5

mat_white = bpy.data.materials.new(name="Colchón Blanco")
mat_white.diffuse_color = (1, 1, 1)

# Crea la estructura de madera
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
obj_cama = bpy.context.active_object
obj_cama.name = "Cama de Matrimonio"
obj_cama.data.materials.append(mat_wood)

# Crea la base de la cama
bpy.ops.mesh.primitive_cube_add(size=1.6, location=(0, -1, 0))
base_cama = bpy.context.active_object
base_cama.name = "Base de la Cama"
base_cama.data.materials.append(mat_wood)

# Crea las patas de la cama
bpy.ops.mesh.primitive_cube_add(size=0.2, location=(-0.8, -1, 0))
pata_cama = bpy.context.active_object
pata_cama.name = "Pata Izquierda"
pata_cama.data.materials.append(mat_wood)

bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0.8, -1, 0))
pata_cama = bpy.context.active_object
pata_cama.name = "Pata Derecha"
pata_cama.data.materials.append(mat_wood)

# Crea el colchón
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.5))
colchon = bpy.context.active_object
colchon.name = "Colchón"
colchon.data.materials.append(mat_white)

# Alinea los objetos
obj_cama.location = (0, -1, 0)
base_cama.location = (0, -2, 0)
pata_cama.location = (-0.8, -3, 0)
pata_cama.location = (0.8, -3, 0)

# Guarda el archivo .blend si se especificó la ruta
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])