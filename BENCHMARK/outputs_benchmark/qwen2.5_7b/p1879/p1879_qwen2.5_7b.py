import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)
bpy.ops.mesh.primitive_cube_add(location=(0, 2.5, -1))
sofa.scale = (1.5, 1, 0.3)

# Crear la alfombra
rug = bpy.data.objects.new(name="Rug", object_data=None)
bpy.context.collection.objects.link(rug)
bpy.ops.mesh.primitive_plane_add(location=(0, 2.8, -0.1))
rug.scale = (4, 2, 0.05)

# Crear el mueble de TV
tv_stand = bpy.data.objects.new(name="TVStand", object_data=None)
bpy.context.collection.objects.link(tv_stand)
bpy.ops.mesh.primitive_cube_add(location=(-3, -1, -0.5))
tv_stand.scale = (0.8, 2, 0.3)

# Crear el panel de listones de madera
panel = bpy.data.objects.new(name="Panel", object_data=None)
bpy.context.collection.objects.link(panel)
bpy.ops.mesh.primitive_plane_add(location=(-3, -1, -0.6))
panel.scale = (4, 0.2, 0.05)

# Rotar el panel para que esté vertical
panel.rotation_euler = (1.57, 0, 0)  # 90 grados alrededor del eje X

# Guardar la escena si se especifica BLEND_OUT
if "BLEND_OUT" in bpy.context.scene:
    blend_out_path = bpy.context.scene["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)