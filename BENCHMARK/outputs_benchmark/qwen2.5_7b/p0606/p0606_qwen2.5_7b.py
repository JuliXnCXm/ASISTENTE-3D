import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo de la cama
bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, -0.1))
suelo = bpy.context.object
suelo.scale = (1.6, 2.0, 1.0)
suelo.name = "Suelo"

# Crear el marco de la cama
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, -0.05))
marco = bpy.context.object
marco.scale = (1.6, 2.0, 0.1)
marco.name = "Marco"

# Crear las barras laterales de la cama
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.8, 0, -0.05))
barra_lateral_izquierda = bpy.context.object
barra_lateral_izquierda.scale = (0.1, 2.0, 0.1)
barra_lateral_izquierda.name = "BarraLateralIzquierda"

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.8, 0, -0.05))
barra_lateral_derecha = bpy.context.object
barra_lateral_derecha.scale = (0.1, 2.0, 0.1)
barra_lateral_derecha.name = "BarraLateralDerecha"

# Crear el colchón
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, -0.3))
colchon = bpy.context.object
colchon.scale = (1.6, 2.0, 0.3)
colchon.name = "Colchon"

# Asignar materiales
madera_roble = bpy.data.materials.new(name="MaderaRoble")
madera_roble.diffuse_color = (0.5, 0.4, 0.3, 1)

blanco = bpy.data.materials.new(name="Blanco")
blanco.diffuse_color = (1, 1, 1, 1)

suelo.data.materials.append(madera_roble)
marco.data.materials.append(madera_roble)
barra_lateral_izquierda.data.materials.append(madera_roble)
barra_lateral_derecha.data.materials.append(madera_roble)
colchon.data.materials.append(blanco)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)