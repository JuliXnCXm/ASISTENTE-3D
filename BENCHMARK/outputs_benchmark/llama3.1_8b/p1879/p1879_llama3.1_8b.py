import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el plano de fondo (pared)
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
bpy.context.object.name = "Pared"
bpy.context.object.scale = (10, 1, 1)

# Crea la alfombra
bpy.ops.mesh.primitive_cube_add(size=5, location=(0, -2.5, 0))
bpy.context.object.name = "Alfombra"
bpy.context.object.scale = (5, 0.01, 0.01)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi / 2, 0, 0))

# Crea el sofá
bpy.ops.mesh.primitive_cube_add(size=3, location=(1.5, -2.5, 0))
bpy.context.object.name = "Sofa"
bpy.context.object.scale = (3, 0.01, 0.01)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi / 2, 0, 0))

# Crea el mueble de TV
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(1.5, -3.5, 0))
bpy.context.object.name = "MuebleTV"
bpy.context.object.scale = (1.5, 0.01, 0.01)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi / 2, 0, 0))

# Crea el panel de listones de madera
bpy.ops.mesh.primitive_cube_add(size=10, location=(0, -4, 0))
bpy.context.object.name = "PanelMadera"
bpy.context.object.scale = (1, 0.01, 10)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi / 2, 0, 0))

# Guarda el archivo .blend si se especificó la ruta
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])