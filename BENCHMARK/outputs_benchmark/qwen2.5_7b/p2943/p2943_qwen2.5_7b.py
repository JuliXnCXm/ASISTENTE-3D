import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la cubierta a dos aguas
base_length = 12.0  # Longitud de la base en metros
base_width = 8.0    # Ancho de la base en metros
height_roof_peak = 3.0  # Altura de la cumbrera en metros
roof_thickness = 0.25  # Espesor de la cubierta en metros

# Crear el piso (base)
bpy.ops.mesh.primitive_plane_add(size=base_length, location=(0, 0, -height_roof_peak / 2))
floor = bpy.context.object
floor.name = "Floor"

# Crear las paredes laterales
wall_height = height_roof_peak + roof_thickness
bpy.ops.mesh.primitive_plane_add(size=base_width, location=(-base_length / 2, base_width / 2, wall_height / 2))
bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z')
bpy.ops.transform.translate(value=(0, -base_length / 2, 0))

wall = bpy.context.object
wall.name = "Wall"

# Crear la cubierta a dos aguas
roof = bpy.ops.mesh.primitive_cylinder_add(radius=base_width / 2, depth=height_roof_peak + roof_thickness, location=(0, 0, wall_height / 2))
bpy.context.object.name = "Roof"
bpy.ops.transform.resize(value=(base_length / (2 * base_width), 1, 1))

# Ajustar la altura de las paredes para que coincidan con el borde superior de la cubierta
wall.location.z += height_roof_peak + roof_thickness

# Guardar el archivo .blend si existe la variable BLEND_OUT
if "BLEND_OUT" in bpy.context.scene:
    blend_out = bpy.context.scene[BLEND_OUT]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)