import bpy
import bmesh

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear terreno de césped
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
terreno = bpy.context.object
terreno.scale.x = 20
terreno.scale.y = 20
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Crear casa de dos pisos
bpy.ops.mesh.primitive_cube_add(size=1, location=(5, -4, 0))
casa = bpy.context.object
casa.scale.x = 10
casa.scale.y = 8
casa.scale.z = 6
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Crear tejado a dos aguas
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=5, depth=6, location=(0, 0, 6))
tejado = bpy.context.object
tejado.rotation_euler = (0, 0, 0.785)  # 45 grados
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# Crear árboles
for i in range(2):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3, location=(i * 10 - 5, -4, 0))
    árbol = bpy.context.object
    árbol.scale.x = 2
    árbol.scale.y = 6
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Guardar .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])