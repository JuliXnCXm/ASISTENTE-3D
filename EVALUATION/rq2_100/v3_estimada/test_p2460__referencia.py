import bpy

# --- Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Definición de parámetros
ancho_escalon = 1.0
huella = 0.3
contrahuella = 0.18
numero_escalones = 5

escalones_creados = []

# --- Creación de cada escalón
for i in range(numero_escalones):
    loc_x = i * huella + huella / 2
    loc_z = i * contrahuella + contrahuella / 2
    
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(loc_x, 0, loc_z),
        scale=(huella, ancho_escalon, contrahuella)
    )
    escalon = bpy.context.active_object
    escalon.name = f'Escalon_{i+1:02d}'
    escalones_creados.append(escalon)

# --- Unión de los escalones en un solo objeto
if len(escalones_creados) > 1:
    bpy.ops.object.select_all(action='DESELECT')
    for escalon in escalones_creados:
        escalon.select_set(True)
    
    bpy.context.view_layer.objects.active = escalones_creados[0]
    bpy.ops.object.join()
    tramo_escalera = bpy.context.active_object
    tramo_escalera.name = 'Tramo_Escalera_Recta'