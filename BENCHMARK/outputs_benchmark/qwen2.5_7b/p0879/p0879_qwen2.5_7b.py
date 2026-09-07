import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el piso
bpy.ops.mesh.primitive_plane_add(size=13, location=(0, 0, -0.1))
bpy.context.object.scale = (4, 3.5, 1)
bpy.ops.object.shade_smooth()

# Pintar el suelo de gris
bpy.ops.paint.weight_paint_toggle()
bpy.ops.paint.weight_paint_clear()
bpy.ops.paint.weight_paint(value=1)

# Crear las paredes
walls = [
    {"x": -2, "y": 3.5/2, "z": 4},
    {"x": 2, "y": 3.5/2, "z": 4},
    {"x": -2, "y": -3.5/2, "z": 4},
    {"x": 2, "y": -3.5/2, "z": 4}
]

for wall in walls:
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(wall["x"], wall["y"], wall["z"]))
    bpy.context.object.scale = (4+0.2, 0.1, 3)
    bpy.ops.object.shade_smooth()

# Pintar las paredes de gris
for i, wall in enumerate(walls):
    bpy.data.objects[f"Cube.{i}"].data.materials.append(bpy.data.materials.new(name=f"Wall{i+1}"))
    bpy.context.object.active_material.diffuse_color = (0.53, 0.53, 0.53, 1)

# Crear la cama doble
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -1, 0))
bpy.context.object.scale = (1.8, 1.6, 0.1)
bpy.ops.object.shade_smooth()

# Crear el armario de dos puertas
bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.5, 0, 0))
bpy.context.object.scale = (0.3, 1.8, 2.2)
bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cube_add(size=0.6, location=(-2.4, 0, 1.9))
bpy.context.object.scale = (0.5, 0.5, 0.3)
bpy.ops.mesh.primitive_cube_add(size=0.6, location=(-2.4, 0, 0.1))
bpy.context.object.scale = (0.5, 0.5, 0.3)

# Guardar el archivo .blend si existe BLEND_OUT
if "BLEND_OUT" in bpy.context.scene:
    blend_out_path = bpy.context.scene["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)