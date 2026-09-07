import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la pérgola
pergola_width = 4.0  # metros
pergola_depth = 3.0  # metros
post_width = 0.2  # metros
post_height = 2.5  # metros
beam_height = 0.2  # metros
beam_depth = 0.2  # metros

# Crear postes
post_locations = [
    (-pergola_width / 2, -pergola_depth / 2, post_height / 2),
    (pergola_width / 2, -pergola_depth / 2, post_height / 2),
    (-pergola_width / 2, pergola_depth / 2, post_height / 2),
    (pergola_width / 2, pergola_depth / 2, post_height / 2)
]

for i, location in enumerate(post_locations):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location,
        rotation=(0, 0, 0)
    )
    post = bpy.context.object
    post.scale = (post_width / 2, post_width / 2, post_height / 2)
    post.name = f"Post_{i+1}"

# Crear vigas principales (largo de la pérgola)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-pergola_width / 2, 0, post_height + beam_height / 2),
    rotation=(0, 0, 0)
)
main_beam1 = bpy.context.object
main_beam1.scale = (pergola_width / 2, beam_depth / 2, beam_height / 2)
main_beam1.name = "Main_Beam_1"

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(pergola_width / 2, 0, post_height + beam_height / 2),
    rotation=(0, 0, 0)
)
main_beam2 = bpy.context.object
main_beam2.scale = (pergola_width / 2, beam_depth / 2, beam_height / 2)
main_beam2.name = "Main_Beam_2"

# Crear vigas transversales (ancho de la pérgola)
num_transverse_beams = 5
transverse_beam_spacing = pergola_depth / (num_transverse_beams + 1)

for i in range(num_transverse_beams):
    location_x = -pergola_width / 2 + (i + 1) * (pergola_depth / (num_transverse_beams + 1)) * 2
    location_y = 0
    location_z = post_height + beam_height / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location_x, location_y, location_z),
        rotation=(0, 0, 0)
    )
    transverse_beam = bpy.context.object
    transverse_beam.scale = (beam_depth / 2, beam_height / 2, pergola_width / 2)
    transverse_beam.name = f"Transverse_Beam_{i+1}"

# Opcional: Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])