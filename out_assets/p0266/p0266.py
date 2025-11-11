import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configuración de escena
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_banco = 1.8
ancho_tablon = 0.1
grosor_tablon = 0.04
altura_asiento = 0.45
separacion_tablones = 0.02
grosor_pata = 0.05
ancho_pata = 0.5
altura_respaldo = 0.4

# Crear tablones del asiento
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(
        location=(0, i * (ancho_tablon + separacion_tablones) - (ancho_tablon + separacion_tablones) * 1.5, altura_asiento),
        scale=(largo_banco / 2, ancho_tablon / 2, grosor_tablon / 2)
    )
    bpy.context.object.name = f"TablonAsiento_{i+1}"

# Crear tablones del respaldo
for i in range(3):
    bpy.ops.mesh.primitive_cube_add(
        location=(0, ancho_pata - grosor_pata, altura_asiento + grosor_tablon + i * (ancho_tablon + separacion_tablones) + 0.1),
        scale=(largo_banco / 2, grosor_tablon / 2, ancho_tablon / 2)
    )
    obj = bpy.context.object
    obj.name = f"TablonRespaldo_{i+1}"
    obj.rotation_euler[0] = 1.5708 * 0.2 # Inclinación de 10 grados aprox.

# Crear patas
posiciones_patas = [-largo_banco / 2 + 0.1, largo_banco / 2 - 0.1]
for pos_x in posiciones_patas:
    # Pata vertical
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, (ancho_pata - grosor_pata)/2, (altura_asiento-grosor_pata)/2),
        scale=(grosor_pata / 2, (ancho_pata - grosor_pata)/2, (altura_asiento-grosor_pata)/2)
    )
    bpy.context.object.name = f"PataVertical_{pos_x}"
    
    # Pata horizontal (base)
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, (ancho_pata - grosor_pata)/2, grosor_pata/2),
        scale=(grosor_pata / 2, ancho_pata / 2, grosor_pata / 2)
    )
    bpy.context.object.name = f"PataBase_{pos_x}"