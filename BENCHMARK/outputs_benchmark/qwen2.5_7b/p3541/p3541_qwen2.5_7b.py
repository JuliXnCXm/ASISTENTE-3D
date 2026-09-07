import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo de deck de madera
deck = bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.2))
deck_obj = bpy.context.object
deck_obj.name = "Deck"
deck_material = bpy.data.materials.new(name="Deck_Material")
deck_material.diffuse_color = (0.8, 0.4, 0.2, 1)
deck_obj.data.materials.append(deck_material)

# Crear las jardineras perimetrales de hormigón
for i in range(4):
    wall_height = 0.5
    wall_width = 0.3
    wall_length = 9.8 if i % 2 == 0 else 10.2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-5 + (i % 2) * 4.9 - 0.15, -2.4 + (i // 2) * 5, wall_height))
    wall_obj = bpy.context.object
    wall_obj.name = f"Jardinera_{i}"
    wall_material = bpy.data.materials.new(name="Hormigon_Material")
    wall_material.diffuse_color = (0.3, 0.3, 0.3, 1)
    wall_obj.data.materials.append(wall_material)

# Crear la vegetación en las jardineras
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(-5 + (i % 2) * 4.9 - 0.1, -2.4 + (i // 2) * 5, wall_height / 2))
    plant_obj = bpy.context.object
    plant_material = bpy.data.materials.new(name="Plant_Material")
    plant_material.diffuse_color = (0.3, 1, 0.3, 1)
    plant_obj.data.materials.append(plant_material)

# Crear la pérgola metálica
pergola_height = 4
pergola_width = 6
pergola_length = 8

bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.5, -0.5, pergola_height / 2))
top_left_pole = bpy.context.object
top_left_pole.name = "Pergola_Top_Left"
top_left_pole.scale *= (pergola_length / 2, pergola_width / 2, 1)

bpy.ops.mesh.primitive_cube_add(size=1, location=(2.5, -0.5, pergola_height / 2))
top_right_pole = bpy.context.object
top_right_pole.name = "Pergola_Top_Right"
top_right_pole.scale *= (pergola_length / 2, pergola_width / 2, 1)

bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.5, -0.5, -pergola_height / 2))
bottom_left_pole = bpy.context.object
bottom_left_pole.name = "Pergola_Bottom_Left"
bottom_left_pole.scale *= (pergola_length / 2, pergola_width / 2, 1)

bpy.ops.mesh.primitive_cube_add(size=1, location=(2.5, -0.5, -pergola_height / 2))
bottom_right_pole = bpy.context.object
bottom_right_pole.name = "Pergola_Bottom_Right"
bottom_right_pole.scale *= (pergola_length / 2, pergola_width / 2, 1)

# Crear las vigas de la pérgola
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-2.5, -0.5, pergola_height))
top_left_viga = bpy.context.object
top_left_viga.name = "Pergola_Top_Left_Viga"
top_left_viga.scale *= (1, 1, pergola_height)

bpy.ops.mesh.primitive_cube_add(size=0.5, location=(2.5, -0.5, pergola_height))
top_right_viga = bpy.context.object
top_right_viga.name = "Pergola_Top_Right_Viga"
top_right_viga.scale *= (1, 1, pergola_height)

bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-2.5, -0.5, -pergola_height))
bottom_left_viga = bpy.context.object
bottom_left_viga.name = "Pergola_Bottom_Left_Viga"
bottom_left_viga.scale *= (1, 1, pergola_height)

bpy.ops.mesh.primitive_cube_add(size=0.5, location=(2.5, -0.5, -pergola_height))
bottom_right_viga = bpy.context.object
bottom_right_viga.name = "Pergola_Bottom_Right_Viga"
bottom_right_viga.scale *= (1, 1, pergola_height)

# Alinear las vigas con los postes
top_left_viga.location = top_left_pole.location + (-pergola_length / 4, -pergola_width / 2, 0)
top_right_viga.location = top_right_pole.location + (pergola_length / 4, -pergola_width / 2, 0)
bottom_left_viga.location = bottom_left_pole.location + (-pergola_length / 4, -pergola_width / 2, 0)
bottom_right_viga.location = bottom_right_pole.location + (pergola_length / 4, -pergola_width / 2, 0)

# Alinear los postes con la pérgola
top_left_pole.location = (-2.5, -0.5, pergola_height)
top_right_pole.location = (2.5, -0.5, pergola_height)
bottom_left_pole.location = (-2.5, -0.5, -pergola_height)
bottom_right_pole.location = (2.5, -0.5, -pergola_height)

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)