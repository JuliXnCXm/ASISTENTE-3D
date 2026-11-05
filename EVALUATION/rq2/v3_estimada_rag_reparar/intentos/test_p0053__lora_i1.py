import bpy
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'
estanteria = bpy.ops.A.crear_estanteria(nombre='EstanteriaPrincipal', ancho=1.2, alto=2.0, fondo=0.35, num_estantes=5, origen=(0, 0, 0), material='Madera')