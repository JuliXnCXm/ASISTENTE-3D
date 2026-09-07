import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear suelo
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, -0.1))
suelo = bpy.context.object
suelo.scale = (8, 6, 1)
suelo.name = "Suelo"

# Zona de estar
bpy.ops.mesh.primitive_cube_add(size=3, location=(-2, 1, 0))
sofá = bpy.context.object
sofá.scale = (1.5, 0.8, 0.2)
sofá.name = "Sofá"

bpy.ops.mesh.primitive_cube_add(size=1, location=(-2, -0.5, 0))
estantería = bpy.context.object
estantería.scale = (3, 0.2, 1)
estantería.name = "Estantería"

# Zona de comedor
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(2, -1, 0))
mesa = bpy.context.object
mesa.scale = (1.5, 1.5, 0.2)
mesa.name = "Mesa"

for i in range(4):
    silla_x = 2 + (i % 2) * 0.7 - 0.35
    silla_y = -1 + int(i / 2) * 0.8 - 0.4
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(silla_x, silla_y, -0.1))
    sillas = [bpy.context.object]
    for silla in sillas:
        silla.scale = (0.6, 0.6, 0.2)
        silla.name = f"Silla_{i}"

# Luz de área
bpy.ops.lighting.new_lamposphere(location=(0, 4, 3))
luz_area = bpy.context.object
luz_area.data.type = 'AREA'
luz_area.data.size = 5
luz_area.name = "LuzArea"

# Guardar el archivo si BLEND_OUT está definido
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)