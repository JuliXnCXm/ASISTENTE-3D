import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

largo = 12.0
ancho = 8.0
altura_cumbrera = 3.0
espesor = 0.25

verts = [
    (largo/2, ancho/2, 0), (-largo/2, ancho/2, 0),
    (-largo/2, -ancho/2, 0), (largo/2, -ancho/2, 0),
    (largo/2, 0, altura_cumbrera), (-largo/2, 0, altura_cumbrera)
]

faces = [
    (0, 1, 5, 4),
    (3, 2, 5, 4)
]

mesh_data = bpy.data.meshes.new('Cubierta_Mesh')
mesh_data.from_pydata(verts, [], faces)
mesh_data.update()

cubierta_obj = bpy.data.objects.new('Cubierta_a_dos_aguas', mesh_data)
bpy.context.collection.objects.link(cubierta_obj)

bpy.context.view_layer.objects.active = cubierta_obj
cubierta_obj.select_set(True)

bpy.ops.object.modifier_add(type='SOLIDIFY')
cubierta_obj.modifiers['Solidify'].thickness = espesor
bpy.ops.object.modifier_apply(modifier='Solidify')