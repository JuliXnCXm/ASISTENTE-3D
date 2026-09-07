import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=20, enter_editmode=False, location=(0, 0, -0.1))
suelo = bpy.context.object
suelo.scale = (16, 20, 1)
suelo.name = "Suelo"

# Crear el marco de la cama
bpy.ops.mesh.primitive_cube_add(size=1.6, enter_editmode=False, location=(0, -0.8, 0))
marco_cama = bpy.context.object
marco_cama.scale = (1.6, 2.0, 0.05)
marco_cama.name = "MarcoCama"

# Crear el colchón
bpy.ops.mesh.primitive_cube_add(size=1.4, enter_editmode=False, location=(0, -0.8, -0.025))
colchon = bpy.context.object
colchon.scale = (1.6, 2.0, 0.05)
colchon.name = "Colchon"

# Asignar materiales
madera_roble = bpy.data.materials.new(name="MaderaRoble")
madera_roble.diffuse_color = (0.4, 0.2, 0.1, 1)

textil_blanco = bpy.data.materials.new(name="TextilBlanco")
textil_blanco.diffuse_color = (1, 1, 1, 1)

marco_cama.data.materials.append(madera_roble)
colchon.data.materials.append(textil_blanco)

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)