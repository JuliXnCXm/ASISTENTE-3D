import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del panel
ancho = 3.0
alto = 5.0
espesor = 0.2

# --- Parámetros de perforación
radio_perf = 0.20
espaciado_x = 0.80
espaciado_y = 0.80

# --- Crear el panel base
bpy.ops.mesh.primitive_cube_add(location=(ancho/2, espesor/2, alto/2))
panel = bpy.context.active_object
panel.name = "PanelFachada"
panel.dimensions = (ancho, espesor, alto)
bpy.ops.object.transform_apply(scale=True)

# --- Crear perforaciones
num_x = int(ancho / espaciado_x)
num_y = int(alto / espaciado_y)

for i in range(num_x):
    for j in range(num_y):
        x = (i + 0.5) * espaciado_x
        z = (j + 0.5) * espaciado_y
        
        # Crear cilindro para cortar
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radio_perf,
            depth=espesor * 1.2, # Un poco más largo para asegurar el corte
            location=(x, espesor/2, z),
            rotation=(1.5708, 0, 0) # 90 grados en X
        )
        cortador = bpy.context.active_object
        
        # Aplicar booleana
        mod = panel.modifiers.new(name=f'Boolean_{i}_{j}', type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = cortador
        bpy.context.view_layer.objects.active = panel
        bpy.ops.object.modifier_apply(modifier=mod.name)
        
        # Eliminar el cortador
        bpy.data.objects.remove(cortador, do_unlink=True)