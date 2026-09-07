import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

bpy.ops.mesh.primitive_cube_add(location=(0, 2.5, -1))
bpy.ops.transform.resize(value=(3, 1, 0.8))

# Crear la alfombra
rug = bpy.data.objects.new(name="Rug", object_data=None)
bpy.context.collection.objects.link(rug)

bpy.ops.mesh.primitive_plane_add(location=(0, -2.5, -0.1))
bpy.ops.transform.resize(value=(4, 3, 0.1))

# Crear el mueble de TV
tv_stand = bpy.data.objects.new(name="TVStand", object_data=None)
bpy.context.collection.objects.link(tv_stand)

bpy.ops.mesh.primitive_cube_add(location=(-2, -1, -0.5))
bpy.ops.transform.resize(value=(1.5, 0.3, 1))

# Crear el fondo de listones de madera
wood_panel = bpy.data.objects.new(name="WoodPanel", object_data=None)
bpy.context.collection.objects.link(wood_panel)

bpy.ops.mesh.primitive_plane_add(location=(-2, -1, -1))
bpy.ops.transform.resize(value=(4, 0.3, 0.1))

# Aplicar materiales (simplificado)
material_sofa = bpy.data.materials.new(name="SofaMaterial")
material_rug = bpy.data.materials.new(name="RugMaterial")
material_tv_stand = bpy.data.materials.new(name="TVStandMaterial")
material_wood_panel = bpy.data.materials.new(name="WoodPanelMaterial")

bpy.context.view_layer.objects.active = sofa
sofa.data.materials.append(material_sofa)

bpy.context.view_layer.objects.active = rug
rug.data.materials.append(material_rug)

bpy.context.view_layer.objects.active = tv_stand
tv_stand.data.materials.append(material_tv_stand)

bpy.context.view_layer.objects.active = wood_panel
wood_panel.data.materials.append(material_wood_panel)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)