import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
escalera_ancho = 10
escalera_largo = 20
rampa_ancho = 3
rampa_largo = 5
jardinera_altura = 0.5
jardinera_profundidad = 1
iluminacion_radio = 2

# Crear la escalinata central
bpy.ops.mesh.primitive_cube_add(size=1, location=(escalera_ancho / 2 - 5, 0, 0))
escalera_central = bpy.context.object
escalera_central.scale = (escalera_largo, escalera_ancho, 0.5)

# Crear las rampas de accesibilidad a ambos lados
bpy.ops.mesh.primitive_cube_add(size=1, location=(escalera_ancho / 2 - 6, 0, 0))
rampa_izquierda = bpy.context.object
rampa_izquierda.scale = (rampa_largo, rampa_ancho, 0.5)

bpy.ops.mesh.primitive_cube_add(size=1, location=(-(escalera_ancho / 2 - 6), 0, 0))
rampa_derecha = bpy.context.object
rampa_derecha.scale = (rampa_largo, rampa_ancho, 0.5)

# Crear las jardineras de hormigón a ambos lados
bpy.ops.mesh.primitive_cube_add(size=1, location=(escalera_ancho / 2 - 6, -jardinera_profundidad / 2, -jardinera_altura))
jardinera_izquierda = bpy.context.object
jardinera_izquierda.scale = (0.5, jardinera_profundidad, jardinera_altura)

bpy.ops.mesh.primitive_cube_add(size=1, location=(escalera_ancho / 2 - 6, jardinera_profundidad / 2, -jardinera_altura))
jardinera_derecha = bpy.context.object
jardinera_derecha.scale = (0.5, jardinera_profundidad, jardinera_altura)

# Añadir iluminación de piso
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -iluminacion_radio))
iluminacion_piso = bpy.context.object
iluminacion_piso.scale = (10, 10, 1)
bpy.ops.object.shade_smooth()
iluminacion_piso.data.materials.append(bpy.data.materials.new(name="Iluminacion"))
material_iluminacion = iluminacion_piso.active_material
material_iluminacion.use_nodes = True
nodes = material_iluminacion.node_tree.nodes
links = material_iluminacion.node_tree.links
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Color'].default_value = (1, 1, 1, 1)
emission_node.inputs['Strength'].default_value = 5
links.new(emission_node.outputs['Emission'], nodes['Material Output'].inputs['Base Color'])

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)