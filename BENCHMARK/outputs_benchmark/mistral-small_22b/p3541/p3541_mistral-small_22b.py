import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo de deck de madera
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
deck = bpy.context.object
deck.name = "Deck"

# Añadir material de madera al deck
material = bpy.data.materials.new(name="WoodMaterial")
material.diffuse_color = (0.8, 0.6, 0.4)
deck.data.materials.append(material)

# Crear jardineras de hormigón
def create_planter(location):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    planter = bpy.context.object
    planter.name = "Planter"
    material = bpy.data.materials.new(name="ConcreteMaterial")
    material.diffuse_color = (0.5, 0.5, 0.5)
    planter.data.materials.append(material)

# Crear vegetación en las jardineras
def create_plant():
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.1, depth=0.5, location=(0, 0, 0))
    plant = bpy.context.object
    plant.name = "Plant"
    material = bpy.data.materials.new(name="GreenMaterial")
    material.diffuse_color = (0, 1, 0)
    plant.data.materials.append(material)

# Crear jardineras en los bordes del deck
planter_locations = [
    (-5, -5, 0), (-5, 5, 0), (5, -5, 0), (5, 5, 0)
]
for location in planter_locations:
    create_planter(location)
    plant = bpy.data.objects["Plant"]
    plant.location = location

# Crear la pérgola metálica
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
pergola = bpy.context.object
pergola.name = "Pergola"
material = bpy.data.materials.new(name="MetalMaterial")
material.diffuse_color = (0.5, 0.5, 0.5)
pergola.data.materials.append(material)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])