import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el suelo base
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
bpy.context.object.scale = (12, 10, 1)

# Crea los bancos de parque
def create_bench():
    # Asiento
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0, 0, 0))
    asiento = bpy.context.object
    asiento.scale = (2, 0.4, 0.1)

    # Respaldo
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0, 0.4, 0))
    respaldo = bpy.context.object
    respaldo.scale = (2, 0.6, 0.1)

    # Soporte de hormigón
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, -0.5, 0))
    soporte = bpy.context.object
    soporte.scale = (2, 0.1, 0.1)

    # Une los objetos en un solo objeto
    bpy.ops.object.select_all(action='DESELECT')
    asiento.select_set(True)
    respaldo.select_set(True)
    soporte.select_set(True)
    bpy.context.view_layer.objects.active = asiento
    bpy.ops.object.join()

# Crea el primer banco
create_bench()
bpy.context.object.location = (4, 0, 0)

# Crea el segundo banco
create_bench()
bpy.context.object.location = (-4, 0, 0)

# Guarda el archivo si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])