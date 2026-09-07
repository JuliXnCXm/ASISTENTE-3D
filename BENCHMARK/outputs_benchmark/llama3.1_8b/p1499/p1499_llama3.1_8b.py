import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el terreno de césped
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
cortadora_cesped = bpy.data.objects['Plane']
cortadora_cesped.name = 'Césped'
cortadora_cesped.scale = (5, 5, 1)
bpy.context.collection.objects.link(cortadora_cesped)

# Crea el árbol
bpy.ops.mesh.primitive_cylinder_add(radius=2, depth=10, location=(0, -3, 0))
arbol = bpy.data.objects['Cylinder']
arbol.name = 'Árbol'
arbol.scale = (1, 1, 1)
bpy.context.collection.objects.link(arbol)

# Crea el banco de madera
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -5, 0))
banco = bpy.data.objects['Cube']
banco.name = 'Banco'
banco.scale = (1.5, 1.5, 1)
bpy.context.collection.objects.link(banco)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])