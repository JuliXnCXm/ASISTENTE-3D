import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del ladrillo y la junta en metros
ladrillo_largo = 0.24
ladrillo_ancho = 0.12
ladrillo_alto = 0.06
junta = 0.01

# Crear un solo ladrillo en el origen
bpy.ops.mesh.primitive_cube_add(size=1, location=(ladrillo_largo / 2, ladrillo_ancho / 2, ladrillo_alto / 2))
ladrillo_obj = bpy.context.active_object
ladrillo_obj.name = "LadrilloBase"
ladrillo_obj.dimensions = (ladrillo_largo, ladrillo_ancho, ladrillo_alto)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Añadir modificador Array para la fila
mod_array_x = ladrillo_obj.modifiers.new(name="ArrayFila", type='ARRAY')
mod_array_x.relative_offset_displace[0] = (ladrillo_largo + junta) / ladrillo_largo
mod_array_x.count = int(8.0 / (ladrillo_largo + junta))

# Añadir modificador Array para la altura
mod_array_z = ladrillo_obj.modifiers.new(name="ArrayAltura", type='ARRAY')
mod_array_z.relative_offset_displace[0] = 0
mod_array_z.relative_offset_displace[2] = (ladrillo_alto + junta) / ladrillo_alto
mod_array_z.count = int(2.5 / (ladrillo_alto + junta))

# Desfase de la hilada (aparejo a soga)
mod_array_z.relative_offset_displace[0] = ((ladrillo_largo + junta) / 2) / (ladrillo_largo * mod_array_x.count)

# Mover el muro para que su base comience en z=0
ladrillo_obj.location.z = 0