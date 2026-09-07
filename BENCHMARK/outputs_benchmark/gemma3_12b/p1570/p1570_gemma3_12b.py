import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la caseta
ancho = 4.0  # metros
fondo = 3.0  # metros
altura_pared = 2.0  # metros
altura_tejado = 1.5  # metros

# Crear la base de la caseta
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura_pared / 2), scale=(ancho, fondo, altura_pared))
base = bpy.context.object
base.name = "Base"

# Crear el primer lado del tejado
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(ancho / 2, fondo / 2, altura_pared + altura_tejado / 2), scale=(1, 1, 1))
lado_tejado_1 = bpy.context.object
lado_tejado_1.name = "LadoTejado1"
lado_tejado_1.rotation_euler[0] = math.radians(45)

# Escalar el lado del tejado para que coincida con la longitud del techo
lado_tejado_1.scale[0] = math.sqrt((ancho / 2)**2 + altura_tejado**2)
lado_tejado_1.scale[1] = 1
lado_tejado_1.scale[2] = 1

# Crear el segundo lado del tejado
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(-ancho / 2, fondo / 2, altura_pared + altura_tejado / 2), scale=(1, 1, 1))
lado_tejado_2 = bpy.context.object
lado_tejado_2.name = "LadoTejado2"
lado_tejado_2.rotation_euler[0] = math.radians(-45)

# Escalar el lado del tejado para que coincida con la longitud del techo
lado_tejado_2.scale[0] = math.sqrt((ancho / 2)**2 + altura_tejado**2)
lado_tejado_2.scale[1] = 1
lado_tejado_2.scale[2] = 1


# Unir los lados del tejado
bpy.ops.object.select_all(action='DESELECT')
lado_tejado_1.select_set(True)
lado_tejado_2.select_set(True)
bpy.context.view_layer.objects.active = lado_tejado_1
bpy.ops.object.join()
tejado = bpy.context.object
tejado.name = "Tejado"

# Mover el tejado a la parte superior de la base
tejado.location = (0, 0, altura_pared)

# Opcional: Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])