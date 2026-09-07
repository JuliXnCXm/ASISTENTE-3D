import bpy

# --- Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# --- Crear el suelo de la plaza
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
suelo = bpy.context.active_object
suelo.name = 'Suelo_Plaza'
suelo.dimensions = (12.0, 10.0, 0)

# --- Función para crear un banco
def crear_banco(nombre, ubicacion):
    # Dimensiones
    largo, ancho, alto_asiento = 2.0, 0.45, 0.45
    alto_respaldo, espesor_liston = 0.4, 0.05
    soporte_ancho, soporte_alto, soporte_espesor = 0.4, 0.4, 0.1

    # Crear objeto padre (vacío) para el banco
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=ubicacion)
    banco_padre = bpy.context.active_object
    banco_padre.name = nombre

    # Soportes de hormigón
    for i in [-1, 1]:
        pos_x = (largo/2 - soporte_espesor*2) * i
        bpy.ops.mesh.primitive_cube_add(location=(pos_x, 0, soporte_alto/2))
        soporte = bpy.context.active_object
        soporte.name = f'Soporte_{i}'
        soporte.dimensions = (soporte_espesor, soporte_ancho, soporte_alto)
        soporte.parent = banco_padre

    # Asiento (listones)
    for i in range(4):
        pos_y = -ancho/2 + espesor_liston/2 + i * (espesor_liston + 0.02)
        bpy.ops.mesh.primitive_cube_add(location=(0, pos_y, alto_asiento))
        liston_asiento = bpy.context.active_object
        liston_asiento.name = f'Liston_Asiento_{i}'
        liston_asiento.dimensions = (largo, espesor_liston, espesor_liston)
        liston_asiento.parent = banco_padre
    
    # Respaldo (listones)
    for i in range(2):
        pos_y_resp = -ancho/2 + espesor_liston/2
        pos_z_resp = alto_asiento + espesor_liston/2 + i * (espesor_liston + 0.02)
        bpy.ops.mesh.primitive_cube_add(location=(0, pos_y_resp, pos_z_resp))
        liston_respaldo = bpy.context.active_object
        liston_respaldo.name = f'Liston_Respaldo_{i}'
        liston_respaldo.dimensions = (largo, espesor_liston, espesor_liston)
        liston_respaldo.parent = banco_padre
    
    return banco_padre

# --- Crear y posicionar los bancos
banco1 = crear_banco('Banco_01', (0, -2, 0))
banco2 = crear_banco('Banco_02', (0, 2, 0))
banco2.rotation_euler[2] = 3.14159 # Rotar 180 grados para que se enfrenten