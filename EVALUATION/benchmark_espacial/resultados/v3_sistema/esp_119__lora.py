import bpy
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'
num_pisos = 10
diametro_torre = 16.0
altura_piso = 3.0
altura_total = num_pisos * altura_piso
altura_actual = 0.0
for i in range(num_pisos + 1):
    bpy.ops.mesh.primitive_cylinder_add(radius=diametro_torre / 2, depth=altura_piso if i < num_pisos else 0, location=(0, 0, altura_actual), vertices=128)
    piso = bpy.context.active_object
    piso.name = f"Piso_{i + 1}"
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    mod_extrusion = piso.modifiers['Solidify']
    mod_extrusion.thickness = altura_piso if i < num_pisos else 0
    bpy.context.view_layer.objects.active = piso
    bpy.ops.object.modifier_apply(modifier=mod_extrusion.name)
    altura_actual += altura_piso