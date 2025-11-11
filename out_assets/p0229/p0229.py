import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
tamaño_adoquin = 0.20
espesor_adoquin = 0.08
separacion = 0.01
area_total = 5.0

# Crear un adoquín base
bpy.ops.mesh.primitive_cube_add(size=1, location=(tamaño_adoquin/2, tamaño_adoquin/2, espesor_adoquin/2))
adoquin_base = bpy.context.active_object
adoquin_base.name = "AdoquinBase"
adoquin_base.dimensions = (tamaño_adoquin, tamaño_adoquin, espesor_adoquin)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Calcular número de adoquines
paso = tamaño_adoquin + separacion
num_adoquines = int(area_total / paso)

# Modificador Array en X
mod_array_x = adoquin_base.modifiers.new(name="ArrayX", type='ARRAY')
mod_array_x.count = num_adoquines
mod_array_x.relative_offset_displace[0] = paso / tamaño_adoquin

# Modificador Array en Y
mod_array_y = adoquin_base.modifiers.new(name="ArrayY", type='ARRAY')
mod_array_y.count = num_adoquines
mod_array_y.relative_offset_displace[0] = 0
mod_array_y.relative_offset_displace[1] = paso / tamaño_adoquin

# Centrar el pavimento en el origen
adoquin_base.location.x = -area_total / 2 + paso/2
adoquin_base.location.y = -area_total / 2 + paso/2
adoquin_base.location.z = 0