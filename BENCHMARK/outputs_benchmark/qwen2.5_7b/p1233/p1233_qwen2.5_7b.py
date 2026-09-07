import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
pisos_altura = 3  # Altura de cada piso en metros (aproximación)
techo_pendiente = 0.5  # Pendiente del techo (altura por metro de longitud)
terreno_ancho, terreno_largo = 20, 20
casa_ancho, casa_largo = 10, 8

# Crear el terreno de césped
bpy.ops.mesh.primitive_plane_add(size=terreno_largo * 2, location=(0, 0, -pisos_altura))
bpy.context.object.scale = (terreno_ancho / bpy.context.object.dimensions.x, terreno_ancho / bpy.context.object.dimensions.x, 1)

# Crear la casa
bpy.ops.mesh.primitive_cube_add(size=1, location=((casa_largo / 2 - 5), (casa_ancho / 2 - 4), pisos_altura))
bpy.context.object.scale = (casa_largo / bpy.context.object.dimensions.x, casa_ancho / bpy.context.object.dimensions.y, pisos_altura)

# Crear el techo a dos aguas
techo_pendiente *= casa_largo
techo = bpy.ops.mesh.primitive_cone_add(radius1=casa_largo / 2, depth=techo_pendiente, location=(0, 0, pisos_altura))
bpy.context.object.scale = (casa_largo / bpy.context.object.dimensions.x, casa_ancho / bpy.context.object.dimensions.y, techo_pendiente)

# Ajustar la posición del techo
bpy.ops.transform.translate(value=(0, 0, -techo_pendiente / 2))

# Crear los árboles
def crear_arbol(x, y):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=(x, y, 4))
    bpy.ops.transform.resize(value=(0.3, 0.3, 0.3))

crear_arbol(-7, -8)
crear_arbol(7, 8)

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.data.filepath.replace('.blend', '_output.blend'))