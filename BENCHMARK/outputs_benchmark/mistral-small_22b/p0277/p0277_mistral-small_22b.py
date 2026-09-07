import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear los postes
poste_size = (0.2, 0.2, 2.5)
for x in [0, 4]:
    for y in [0, 3]:
        bpy.ops.mesh.primitive_cube_add(size=poste_size, location=(x, y, poste_size[2] / 2))

# Crear las vigas principales
viga_principal_size = (4, 0.1, 0.1)
bpy.ops.mesh.primitive_cube_add(size=viga_principal_size, location=(2, 0, poste_size[2] + viga_principal_size[2] / 2))
bpy.ops.mesh.primitive_cube_add(size=viga_principal_size, location=(2, 3, poste_size[2] + viga_principal_size[2] / 2))

# Crear las vigas transversales
viga_transversal_size = (0.1, 3, 0.1)
for z in range(5):
    bpy.ops.mesh.primitive_cube_add(size=viga_transversal_size, location=(2, z * viga_transversal_size[1] / 4 + 1.5, poste_size[2] + viga_principal_size[2] / 2))

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])