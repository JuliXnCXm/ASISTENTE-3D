import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
largo_banco = 2.0
profundidad_banco = 0.6
altura_total = 0.8
altura_asiento = 0.45
grosor_pata = 0.05
grosor_tablon = 0.04

# Patas de acero
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * (largo_banco / 2 - grosor_pata), 0, altura_asiento / 2),
        scale=(grosor_pata, grosor_pata, altura_asiento)
    )
    bpy.context.active_object.name = f"PataFrontal_{'Izq' if i == -1 else 'Der'}"
    
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * (largo_banco / 2 - grosor_pata), profundidad_banco - grosor_pata, altura_total / 2),
        scale=(grosor_pata, grosor_pata, altura_total)
    )
    bpy.context.active_object.name = f"PataTrasera_{'Izq' if i == -1 else 'Der'}"

# Tablones del asiento
num_tablones_asiento = 4
ancho_tablon = (profundidad_banco - 0.05) / num_tablones_asiento
for i in range(num_tablones_asiento):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, i * (ancho_tablon + 0.01) + ancho_tablon / 2, altura_asiento),
        scale=(largo_banco, ancho_tablon, grosor_tablon)
    )
    bpy.context.active_object.name = f"TablonAsiento_{i+1}"

# Tablones del respaldo
num_tablones_respaldo = 2
for i in range(num_tablones_respaldo):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, profundidad_banco - grosor_pata, altura_asiento + 0.15 + i * (ancho_tablon + 0.02)),
        scale=(largo_banco, grosor_tablon, ancho_tablon)
    )
    bpy.context.active_object.name = f"TablonRespaldo_{i+1}"