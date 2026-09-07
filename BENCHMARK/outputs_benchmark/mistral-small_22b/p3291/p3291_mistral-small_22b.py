import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo de deck de madera
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
deck = bpy.context.object
deck.name = "Deck"

# Crear las jardineras perimetrales de hormigón
for i in range(-5, 6):
    for j in range(-5, 6):
        if abs(i) == 5 or abs(j) == 5:
            bpy.ops.mesh.primitive_cube_add(size=0.2, location=(i, j, 0))
            planter = bpy.context.object
            planter.name = "Planter"

# Crear la pérgola de acero
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -2, 3))
pergola = bpy.context.object
pergola.name = "Pergola"

# Añadir vegetación variada a las jardineras
for planter in bpy.data.objects:
    if planter.name == "Planter":
        bpy.ops.mesh.primitive_cone_add(vertices=32, radius=0.1, depth=0.5, location=(planter.location.x, planter.location.y, 0.1))
        tree = bpy.context.object
        tree.name = "Tree"

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])