import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear postes de 0.2x0.2x2.5 m en las esquinas
for x in [1, -1]:
    for z in [1.5, -1.5]:
        bpy.ops.mesh.primitive_cube_add(size=0.2, location=(x * 2, 0, z * 2.5))

# Crear vigas principales de 4x0.2x0.2 m
bpy.ops.mesh.primitive_cube_add(size=0.2, location=(-1, 1.5, 1))
bpy.ops.mesh.primitive_cube_add(size=0.2, location=(1, 1.5, 1))

# Crear vigas transversales de 3x0.2x0.2 m
for x in [1, -1]:
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(x, 1.5, 0.2))
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(x, 1.5, 2.4))

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.properties.BLEND_OUT)