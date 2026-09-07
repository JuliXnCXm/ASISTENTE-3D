import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
escalera_ancho = 10.0
escalera_largo = 20.0
rampa_ancho = 3.0
rampa_largo = 5.0
jardinera_altura = 0.5
jardinera_ancho = 4.0

# Crear la escalinata central
bpy.ops.mesh.primitive_cube_add(size=1, location=(escalera_ancho / 2 - escalera_largo / 2, 0, -1))
bpy.ops.transform.resize(value=(escalera_largo, escalera_ancho, 1))

# Crear las rampas de accesibilidad
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(rampa_ancho / 2 - rampa_largo / 2 + i * (escalera_ancho + rampa_ancho), 0, -0.5))
    bpy.ops.transform.resize(value=(rampa_largo, rampa_ancho, 1))

# Crear las jardineras
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(escalera_ancho / 2 + i * (escalera_ancho + rampa_ancho), -jardinera_ancho / 2, -0.5))
    bpy.ops.transform.resize(value=(jardinera_ancho, jardinera_ancho, jardinera_altura))

# Crear la iluminación de piso
bpy.ops.mesh.primitive_plane_add(size=escalera_largo + rampa_largo * 2, location=(0, -1.5, -1))
bpy.ops.object.shade_smooth()
bpy.context.object.active_material = bpy.data.materials.new(name="FloorLight")
bpy.context.object.active_material.use_nodes = True
nodes = bpy.context.object.active_material.node_tree.nodes
links = bpy.context.object.active_material.node_tree.links
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Color'].default_value = (1, 1, 1, 1)
emission_node.inputs['Strength'].default_value = 5.0
nodes_links = links.new(emission_node.outputs['Emission'], nodes['Material Output'].inputs['Base Color'])

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)