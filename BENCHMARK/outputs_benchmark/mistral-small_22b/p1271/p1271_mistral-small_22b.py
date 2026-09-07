import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear terreno de césped
terreno = bpy.data.objects.new("Terreno", None)
bpy.context.collection.objects.link(terreno)
terreno.location = (0, 0, 0)
terreno = bpy.data.meshes.new("Terreno")
terreno_obj = bpy.data.objects.new("Terreno", terreno)
bpy.context.collection.objects.link(terreno_obj)
terreno = terreno_obj.data
terreno.vertices.new((-12.5, -10, 0))
terreno.vertices.new((-12.5, 10, 0))
terreno.vertices.new((12.5, -10, 0))
terreno.vertices.new((12.5, 10, 0))
terreno.vertices.new((-12.5, -10, 1))
terreno.vertices.new((-12.5, 10, 1))
terreno.vertices.new((12.5, -10, 1))
terreno.vertices.new((12.5, 10, 1))
terreno.polygons.new([0, 1, 2, 3])
terreno.polygons.new([4, 5, 6, 7])
terreno.polygons.new([0, 1, 5, 4])
terreno.polygons.new([2, 3, 7, 6])
terreno.polygons.new([0, 2, 6, 4])
terreno.polygons.new([1, 3, 7, 5])
terreno_obj.select_set(True)
bpy.context.view_layer.objects.active = terreno_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=10)
bpy.ops.object.mode_set(mode='OBJECT')
terreno_obj.select_set(False)

# Crear casa de campo
casa = bpy.data.objects.new("Casa", None)
bpy.context.collection.objects.link(casa)
casa.location = (0, 0, 0)
casa = bpy.data.meshes.new("Casa")
casa_obj = bpy.data.objects.new("Casa", casa)
bpy.context.collection.objects.link(casa_obj)
casa = casa_obj.data
casa.vertices.new((-6, -4.5, 0))
casa.vertices.new((-6, 4.5, 0))
casa.vertices.new((6, -4.5, 0))
casa.vertices.new((6, 4.5, 0))
casa.vertices.new((-6, -4.5, 3))
casa.vertices.new((-6, 4.5, 3))
casa.vertices.new((6, -4.5, 3))
casa.vertices.new((6, 4.5, 3))
casa.polygons.new([0, 1, 2, 3])
casa.polygons.new([4, 5, 6, 7])
casa.polygons.new([0, 1, 5, 4])
casa.polygons.new([2, 3, 7, 6])
casa_obj.select_set(True)
bpy.context.view_layer.objects.active = casa_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_shrink_fatten={"value":0.5})
bpy.ops.object.mode_set(mode='OBJECT')
casa_obj.select_set(False)

# Crear tejado a dos aguas
tejado = bpy.data.objects.new("Tejado", None)
bpy.context.collection.objects.link(tejado)
tejado.location = (0, 0, 3)
tejado = bpy.data.meshes.new("Tejado")
tejado_obj = bpy.data.objects.new("Tejado", tejado)
bpy.context.collection.objects.link(tejado_obj)
tejado = tejado_obj.data
tejado.vertices.new((-6, -4.5, 0))
tejado.vertices.new((-6, 4.5, 0))
tejado.vertices.new((6, -4.5, 0))
tejado.vertices.new((6, 4.5, 0))
tejado.vertices.new((-3, 0, 2))
tejado.vertices.new((3, 0, 2))
tejado.polygons.new([0, 1, 4])
tejado.polygons.new([1, 2, 5])
tejado.polygons.new([2, 3, 4])
tejado_obj.select_set(True)
bpy.context.view_layer.objects.active = tejado_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=10)
bpy.ops.object.mode_set(mode='OBJECT')
tejado_obj.select_set(False)

# Crear árbol
arbol = bpy.data.objects.new("Arbol", None)
bpy.context.collection.objects.link(arbol)
arbol.location = (-10, -5, 0)
arbol = bpy.data.meshes.new("Arbol")
arbol_obj = bpy.data.objects.new("Arbol", arbol)
bpy.context.collection.objects.link(arbol_obj)
arbol = arbol_obj.data
arbol.vertices.new((0, 0, 0))
arbol.edges.new([0, 1])
arbol_obj.select_set(True)
bpy.context.view_layer.objects.active = arbol_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_shrink_fatten={"value":1})
bpy.ops.object.mode_set(mode='OBJECT')
arbol_obj.select_set(False)

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])