import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el colchón blanco
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.5))
colchon = bpy.context.object
colchon.scale = (2, 2, 0.1)  # Ajustar tamaño para que parezca un colchón
colchon.name = "Colchon"
bpy.ops.object.shade_smooth()
bpy.data.objects["Colchon"].data.materials.append(bpy.data.materials.new(name="Blanco"))
bpy.context.active_object.active_material.diffuse_color = (1, 1, 1, 1)

# Crear la estructura de madera
bpy.ops.mesh.primitive_cube_add(size=0.25, location=(0, -0.75, 0))
estructura_izquierda = bpy.context.object
estructura_izquierda.scale = (0.1, 1.5, 0.1)
estructura_izquierda.name = "EstructuraIzquierda"
bpy.ops.mesh.primitive_cube_add(size=0.25, location=(0, 0.75, 0))
estructura_derecha = bpy.context.object
estructura_derecha.scale = (0.1, 1.5, 0.1)
estructura_derecha.name = "EstructuraDerecha"
bpy.ops.mesh.primitive_cube_add(size=2, location=(0.75, 0, -0.1))
cabecera = bpy.context.object
cabecera.scale = (0.3, 1.5, 0.1)
cabecera.name = "Cabecera"
bpy.ops.mesh.primitive_cube_add(size=2, location=(-0.75, 0, -0.1))
pie = bpy.context.object
pie.scale = (0.3, 1.5, 0.1)
pie.name = "Pie"

# Asignar material de madera a la estructura
bpy.data.objects["EstructuraIzquierda"].data.materials.append(bpy.data.materials.new(name="MaderaRoble"))
bpy.context.active_object.active_material.diffuse_color = (0.5, 0.3, 0.1, 1)
bpy.data.objects["EstructuraDerecha"].data.materials.append(bpy.data.materials.new(name="MaderaRoble"))
bpy.context.active_object.active_material.diffuse_color = (0.5, 0.3, 0.1, 1)
bpy.data.objects["Cabecera"].data.materials.append(bpy.data.materials.new(name="MaderaRoble"))
bpy.context.active_object.active_material.diffuse_color = (0.5, 0.3, 0.1, 1)
bpy.data.objects["Pie"].data.materials.append(bpy.data.materials.new(name="MaderaRoble"))
bpy.context.active_object.active_material.diffuse_color = (0.5, 0.3, 0.1, 1)

# Guardar el archivo si BLEND_OUT está definido
if "BLEND_OUT" in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene["BLEND_OUT"])