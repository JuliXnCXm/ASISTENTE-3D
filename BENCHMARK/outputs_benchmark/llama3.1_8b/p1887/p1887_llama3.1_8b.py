import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del escritorio en metros
escritorio_ancho = 1.5
escritorio_fondo = 0.8
escritorio_profundidad = 0.6

# Crea el cuerpo principal del escritorio
bpy.ops.mesh.primitive_cube_add(size=escritorio_profundidad, location=(0, -escritorio_ancho/2, 0))
escritorio_cuerpo = bpy.context.active_object
escritorio_cuerpo.scale = (escritorio_ancho, escritorio_fondo, escritorio_profundidad)

# Crea la parte trasera del escritorio
bpy.ops.mesh.primitive_cube_add(size=escritorio_profundidad, location=(0, -escritorio_ancho/2, -escritorio_fondo))
trasera = bpy.context.active_object
trasera.scale = (escritorio_ancho, escritorio_fondo, escritorio_profundidad)

# Combina las dos partes del escritorio en una sola pieza
bpy.ops.object.join()

# Define las dimensiones de la silla de oficina en metros
silla_ancho = 0.5
silla_fondo = 0.4
silla_altura = 0.8

# Crea el cuerpo principal de la silla
bpy.ops.mesh.primitive_cube_add(size=silla_altura, location=(0, -silla_ancho/2, 0))
silla_cuerpo = bpy.context.active_object
silla_cuerpo.scale = (silla_ancho, silla_fondo, silla_altura)

# Crea la parte trasera de la silla
bpy.ops.mesh.primitive_cube_add(size=silla_altura, location=(0, -silla_ancho/2, -silla_fondo))
trasera_silla = bpy.context.active_object
trasera_silla.scale = (silla_ancho, silla_fondo, silla_altura)

# Combina las dos partes de la silla en una sola pieza
bpy.ops.object.join()

# Define las dimensiones de la estantería de pared en metros
estanteria_ancho = 1.2
estanteria_fondo = 0.6
estanteria_altura = 1.8

# Crea el cuerpo principal de la estantería
bpy.ops.mesh.primitive_cube_add(size=estanteria_altura, location=(0, -estanteria_ancho/2, 0))
estanteria_cuerpo = bpy.context.active_object
estanteria_cuerpo.scale = (estanteria_ancho, estanteria_fondo, estanteria_altura)

# Crea los soportes de la estantería
bpy.ops.mesh.primitive_cube_add(size=estanteria_altura/2, location=(0, -estanteria_ancho/4, 0))
soporte1 = bpy.context.active_object
soporte1.scale = (estanteria_ancho/2, estanteria_fondo, estanteria_altura/2)

bpy.ops.mesh.primitive_cube_add(size=estanteria_altura/2, location=(0, -3*estanteria_ancho/4, 0))
soporte2 = bpy.context.active_object
soporte2.scale = (estanteria_ancho/2, estanteria_fondo, estanteria_altura/2)

# Combina las piezas de la estantería en una sola pieza
bpy.ops.object.join()

# Aplica un modificador para crear el diseño paramétrico de la estantería
mod = bpy.context.active_object.modifiers.new(name="Array", type='ARRAY')
mod.use_merge = True
mod.merge_mode = 'COLLADA'

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])