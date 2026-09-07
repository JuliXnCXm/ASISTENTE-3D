import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la losa y la pérgola
losa_dimensiones = (4.0, 3.0, 0.15)
pergola_poste_dimensiones = (0.15, 0.15, 2.5)
pergola_viga_dimensiones = (0.1, 0.1, 2.5)

# Crea la losa
bpy.ops.mesh.primitive_cube_add(size=losa_dimensiones[0], location=(0, 0, -losa_dimensiones[2]/2))
bpy.context.active_object.name = "Losa"
bpy.ops.object.modifier_apply(modifier="Remesh")

# Crea los postes de la pérgola
poste1 = bpy.data.objects.new("Puesto1", bpy.data.meshes.new("Puesto1"))
poste1.location = (0, 0, -losa_dimensiones[2]/2 + pergola_poste_dimensiones[2])
bpy.context.collection.objects.link(poste1)
bpy.ops.object.modifier_apply(modifier="Remesh")

poste2 = poste1.copy()
poste2.name = "Puesto2"
poste2.location = (losa_dimensiones[0] - 0.15, 0, -losa_dimensiones[2]/2 + pergola_poste_dimensiones[2])
bpy.context.collection.objects.link(poste2)

poste3 = poste1.copy()
poste3.name = "Puesto3"
poste3.location = (0, losa_dimensiones[1] - 0.15, -losa_dimensiones[2]/2 + pergola_poste_dimensiones[2])
bpy.context.collection.objects.link(poste3)

poste4 = poste1.copy()
poste4.name = "Puesto4"
poste4.location = (losa_dimensiones[0] - 0.15, losa_dimensiones[1] - 0.15, -losa_dimensiones[2]/2 + pergola_poste_dimensiones[2])
bpy.context.collection.objects.link(poste4)

# Crea las vigas de la pérgola
viga1 = bpy.data.objects.new("Viga1", bpy.data.meshes.new("Viga1"))
viga1.location = (0, 0, -losa_dimensiones[2]/2 + pergola_viga_dimensiones[2])
bpy.context.collection.objects.link(viga1)
bpy.ops.object.modifier_apply(modifier="Remesh")

viga2 = viga1.copy()
viga2.name = "Viga2"
viga2.location = (losa_dimensiones[0] - 0.15, 0, -losa_dimensiones[2]/2 + pergola_viga_dimensiones[2])
bpy.context.collection.objects.link(viga2)

viga3 = viga1.copy()
viga3.name = "Viga3"
viga3.location = (0, losa_dimensiones[1] - 0.15, -losa_dimensiones[2]/2 + pergola_viga_dimensiones[2])
bpy.context.collection.objects.link(viga3)

viga4 = viga1.copy()
viga4.name = "Viga4"
viga4.location = (losa_dimensiones[0] - 0.15, losa_dimensiones[1] - 0.15, -losa_dimensiones[2]/2 + pergola_viga_dimensiones[2])
bpy.context.collection.objects.link(viga4)

# Conecta las vigas a los postes
bpy.ops.object.select_all(action='DESELECT')
viga1.select_set(True)
poste1.select_set(True)
bpy.context.view_layer.objects.active = viga1
bpy.ops.object.join()

viga2.select_set(True)
poste2.select_set(True)
bpy.context.view_layer.objects.active = viga2
bpy.ops.object.join()

viga3.select_set(True)
poste3.select_set(True)
bpy.context.view_layer.objects.active = viga3
bpy.ops.object.join()

viga4.select_set(True)
poste4.select_set(True)
bpy.context.view_layer.objects.active = viga4
bpy.ops.object.join()

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])