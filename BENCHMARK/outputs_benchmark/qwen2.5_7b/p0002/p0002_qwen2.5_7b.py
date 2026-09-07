import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del muro
largo = 5.0
alto = 2.5
espesor = 0.15

# Crear el muro divisorio interior
bpy.ops.mesh.primitive_cube_add(size=espesor, enter_editmode=False, align='WORLD', location=(largo / 2, alto / 2, espesor / 2))
muro = bpy.context.object
muro.scale = (largo, alto, espesor)

# Alinear el muro en el centro del espacio de trabajo
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.background_save_path)