import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de tres plazas
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

bpy.ops.mesh.primitive_cube_add(location=(0, 1.5, -0.2))
bpy.ops.transform.resize(value=(2, 1.5, 0.8))

bpy.ops.mesh.primitive_cylinder_add(location=(-0.67, 0, -0.2))
bpy.ops.transform.resize(value=(0.33, 1.5, 0.4))
bpy.ops.object.shade_smooth()

bpy.ops.mesh.primitive_cylinder_add(location=(0.67, 0, -0.2))
bpy.ops.transform.resize(value=(0.33, 1.5, 0.4))
bpy.ops.object.shade_smooth()

bpy.ops.mesh.primitive_cube_add(location=(0, 1.5, -0.8))
bpy.ops.transform.resize(value=(2, 0.6, 0.4))
bpy.ops.object.shade_smooth()

sofa.data.materials.append(bpy.data.materials.new(name="TelaGris"))
sofa.active_material.diffuse_color = (0.59, 0.59, 0.59)

# Crear la mesa de centro
table = bpy.data.objects.new(name="Table", object_data=None)
bpy.context.collection.objects.link(table)

bpy.ops.mesh.primitive_cube_add(location=(0, -1.5, 0))
bpy.ops.transform.resize(value=(1, 0.8, 0.2))

bpy.ops.mesh.primitive_cylinder_add(location=(0, -1.5, 0.1))
bpy.ops.transform.resize(value=(0.6, 0.4, 0.3))
bpy.ops.object.shade_smooth()

table.data.materials.append(bpy.data.materials.new(name="MaderaNogal"))
table.active_material.diffuse_color = (0.5, 0.27, 0)

# Posicionar la mesa frente al sofá
bpy.context.view_layer.objects.active = sofa
bpy.ops.object.select_all(action='DESELECT')
sofa.select_set(True)
bpy.ops.transform.translate(value=(0, -3, 0))

if "BLEND_OUT" in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene["BLEND_OUT"])