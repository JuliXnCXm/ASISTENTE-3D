import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define los materiales
asphalt_material = bpy.data.materials.new(name="Asphalt")
asphalt_material.diffuse_color = (0.2, 0.2, 0.2, 1)
acera_material = bpy.data.materials.new(name="Acera")
acera_material.diffuse_color = (0.8, 0.6, 0.4, 1)
baranda_material = bpy.data.materials.new(name="Baranda")
baranda_material.diffuse_color = (0.5, 0.5, 1, 1)

# Asfalto
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, -5, 0))
asphalt = bpy.context.object
asphalt.data.materials.append(asphalt_material)

# Acera
acera_length = 10
acera_width = 2
bpy.ops.mesh.primitive_plane_add(size=acera_width * 2, location=(-acera_width / 2 + acera_length / 2 - acera_width / 4, -5.5, 0))
acera = bpy.context.object
acera.scale = (acera_length, acera_width, 1)
acera.data.materials.append(acera_material)

# Baranda
baranda_height = 1
bpy.ops.mesh.primitive_cube_add(size=2, location=(-acera_width / 4 + acera_length / 2 - acera_width / 8, -5.75, baranda_height / 2))
baranda = bpy.context.object
baranda.scale = (acera_length / 2, acera_width / 2, baranda_height)
baranda.data.materials.append(baranda_material)

# Ajusta la escala a metros
bpy.ops.object.select_all(action='SELECT')
bpy.ops.transform.resize(value=(1, 1, 0.01))

if 'BLEND_OUT' in os.environ:
    bpy.context.scene.render.filepath = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile()