import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el marco de la cama
def create_frame():
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    frame = bpy.context.object
    frame.name = "Frame"

    # Crear las patas
    for i in range(4):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.5, location=(i % 2 * 2 - 2, i // 2 * 2 - 2, 0))
        pata = bpy.context.object
        pata.name = f"Pata_{i}"
        frame.select_set(True)
        pata.select_set(True)
        bpy.context.view_layer.objects.active = frame
        bpy.ops.object.parent_set(type='OBJECT')
        frame.select_set(False)
        pata.select_set(False)

    # Crear la base del colchón
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, -1))
    base = bpy.context.object
    base.name = "Base"
    frame.select_set(True)
    base.select_set(True)
    bpy.context.view_layer.objects.active = frame
    bpy.ops.object.parent_set(type='OBJECT')
    frame.select_set(False)
    base.select_set(False)

create_frame()

# Crear el colchón
def create_mattress():
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, -1))
    mattress = bpy.context.object
    mattress.name = "Mattress"

    # Crear materiales
    mat_wood = bpy.data.materials.new(name="Wood")
    mat_wood.diffuse_color = (0.5, 0.3, 0.1)
    mat_fabric = bpy.data.materials.new(name="Fabric")
    mat_fabric.diffuse_color = (1, 1, 1)

    # Asignar materiales a los objetos
    frame = bpy.data.objects["Frame"]
    mattress = bpy.data.objects["Mattress"]
    base = bpy.data.objects["Base"]

    frame.data.materials.append(mat_wood)
    mattress.data.materials.append(mat_fabric)
    base.data.materials.append(mat_wood)

create_mattress()

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])