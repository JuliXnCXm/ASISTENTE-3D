import bpy
import math

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Parámetros del panel
ancho = 3.0
alto = 5.0
espesor = 0.1
num_x = 8
num_y = 14
radio_max = 0.12
radio_min = 0.03

# Crear el panel base
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2, alto/2, 0))
panel = bpy.context.active_object
panel.name = "PanelFachada"
panel.dimensions = (ancho, alto, espesor)

# Crear cilindros para las perforaciones
step_x = ancho / num_x
step_y = alto / num_y

cilindros_a_restar = []

for i in range(num_x):
    for j in range(num_y):
        x = i * step_x + step_x / 2
        y = j * step_y + step_y / 2
        
        # Interpolar el radio basado en la altura (y)
        factor = y / alto
        radio = radio_max * (1 - factor) + radio_min * factor
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radio,
            depth=espesor * 2, # Asegurar que atraviesa completamente
            location=(x, y, 0),
            rotation=(math.radians(90), 0, 0)
        )
        cilindro = bpy.context.active_object
        cilindro.name = f"Cilindro_{i}_{j}"
        cilindros_a_restar.append(cilindro)

# Aplicar modificadores booleanos
bpy.context.view_layer.objects.active = panel
for cyl in cilindros_a_restar:
    mod = panel.modifiers.new(name=f'Bool_{cyl.name}', type='BOOLEAN')
    mod.object = cyl
    mod.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cyl, do_unlink=True)