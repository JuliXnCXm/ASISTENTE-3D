import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_base = 3.0
altura_borde = 0.4
grosor_borde = 0.15
altura_pedestal = 1.0
radio_pedestal = 0.25

# --- Base tipo anillo (sin bmesh) ---
R = diametro_base / 2
# Cilindro exterior
bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=altura_borde, location=(0, 0, altura_borde/2), vertices=64)
base_ext = bpy.context.active_object
base_ext.name = 'BaseExterior'
# Cilindro interior para vaciar
bpy.ops.mesh.primitive_cylinder_add(radius=max(0.01, R - grosor_borde), depth=altura_borde*1.05, location=(0, 0, altura_borde/2), vertices=64)
base_int = bpy.context.active_object
base_int.name = 'BaseInteriorCorte'
# Booleano diferencia
mod = base_ext.modifiers.new(name='Boolean', type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = base_int
bpy.context.view_layer.objects.active = base_ext
base_ext.select_set(True)
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(base_int, do_unlink=True)

# --- Pedestal central ---
bpy.ops.mesh.primitive_cylinder_add(radius=radio_pedestal, depth=altura_pedestal, location=(0, 0, altura_pedestal/2), vertices=32)
pedestal = bpy.context.active_object
pedestal.name = 'Pedestal'

# --- Surtidor (tazón sencillo a modo decorativo) ---
bpy.ops.mesh.primitive_uv_sphere_add(radius=radio_pedestal*1.5, location=(0, 0, altura_pedestal))
surtidor = bpy.context.active_object
surtidor.name = 'Surtidor'
# Aplastar un poco en Z
bpy.ops.transform.resize(value=(1, 1, 0.5))
