import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir los materiales
cepo_material = bpy.data.materials.new(name="Césped")
cepo_material.use_nodes = True
cepo_principalemission = cepo_material.node_tree.nodes["Principled BSDF"]
cepo_principalemission.inputs['Base Color'].default_value = (0.3, 1, 0.2, 1)
cepo_principalemission.inputs['Roughness'].default_value = 0.5

madera_material = bpy.data.materials.new(name="Madera")
madera_material.use_nodes = True
madera_principalemission = madera_material.node_tree.nodes["Principled BSDF"]
madera_principalemission.inputs['Base Color'].default_value = (0.6, 0.4, 0.2, 1)
madera_principalemission.inputs['Roughness'].default_value = 0.3

# Crear el terreno de césped
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -0.5))
terreno = bpy.context.object
terreno.data.materials.append(cepo_material)

# Crear la casa
bpy.ops.mesh.primitive_cube_add(location=(-4, -1, 0))
casa_base = bpy.context.object
casa_base.scale = (8, 10, 2)
casa_base.data.materials.append(madera_material)

# Crear el tejado a dos aguas
tejado = bpy.ops.archipack_roof.add(archipack=[('roof_type', '2'), ('length', 8), ('width', 10), ('height', 3), ('pitch', 45), ('offset', -1.5), ('extrude', 0.1), ('material', madera_material.name)], location=(-4, -1, 2.5))
tejado = bpy.context.object
tejado.scale = (8, 10, 3)

# Crear los árboles
def crear_arbol(x, y):
    arbol = bpy.ops.archipack_tree.add(location=(x, y, 0), size=2)
    arbol_objeto = bpy.context.object
    arbol_objeto.scale = (1.5, 1.5, 1.5)

crear_arbol(-6, -3)
crear_arbol(6, 3)

# Guardar el archivo si existe BLEND_OUT
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)