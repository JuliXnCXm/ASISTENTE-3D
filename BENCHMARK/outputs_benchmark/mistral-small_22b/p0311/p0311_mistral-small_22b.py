import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el marco de la cama
def create_bed_frame():
    # Crear un cubo para el marco
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    frame = bpy.context.object
    frame.name = "BedFrame"

    # Crear un cubo para la base del marco
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -0.1, 0))
    base = bpy.context.object
    base.name = "Base"

    # Crear un cubo para los postes del marco
    for i in range(4):
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(i % 2 * 1.9 - 0.95, (i // 2) * 1.9 - 0.95, 0))
        post = bpy.context.object
        post.name = f"Post{i}"

    # Crear un cubo para la cabecera del marco
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 1.9, -0.1))
    header = bpy.context.object
    header.name = "Header"

# Crear el colchón de la cama
def create_mattress():
    # Crear un cubo para el colchón
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    mattress = bpy.context.object
    mattress.name = "Mattress"

# Crear la estructura de madera de roble
def create_wood_texture():
    # Crear un nuevo material para la textura de madera
    wood_material = bpy.data.materials.new(name="WoodMaterial")
    wood_material.diffuse_color = (0.6, 0.35, 0.22)  # Color roble

    # Asignar el material a los objetos del marco de la cama
    for obj in bpy.data.objects:
        if "BedFrame" in obj.name or "Post" in obj.name or "Header" in obj.name:
            obj.data.materials.append(wood_material)

# Crear el colchón blanco
def create_white_mattress():
    # Crear un nuevo material para el colchón blanco
    white_material = bpy.data.materials.new(name="WhiteMaterial")
    white_material.diffuse_color = (1, 1, 1)  # Color blanco

    # Asignar el material al objeto del colchón
    mattress = bpy.data.objects["Mattress"]
    mattress.data.materials.append(white_material)

# Crear la cama de matrimonio estándar
create_bed_frame()
create_mattress()
create_wood_texture()
create_white_mattress()

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])