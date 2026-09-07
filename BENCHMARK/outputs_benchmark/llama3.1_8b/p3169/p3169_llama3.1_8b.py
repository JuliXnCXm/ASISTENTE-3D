import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del espacio principal y la sala de reuniones
espacio_principal = (8, 6, 2.8)
sala_reuniones = (3, 4, 2.8)

# Crea el espacio principal
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
objeto_espacio_principal = bpy.context.active_object
objeto_espacio_principal.scale = (espacio_principal[0], espacio_principal[1], espacio_principal[2])

# Crea la sala de reuniones
bpy.ops.mesh.primitive_cube_add(size=1, location=(3.5, 4.5, 0))
objeto_sala_reuniones = bpy.context.active_object
objeto_sala_reuniones.scale = (sala_reuniones[0], sala_reuniones[1], sala_reuniones[2])

# Crea los puestos de trabajo en el espacio principal
for i in range(4):
    # Escritorio
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-3 + 1.75 * i, -3, 2))
    objeto_escritorio = bpy.context.active_object
    objeto_escritorio.scale = (0.5, 0.5, 0.5)
    
    # Silla ergonómica
    bpy.ops.mesh.primitive_cube_add(size=0.25, location=(-3 + 1.75 * i, -2.75, 2))
    objeto_silla_ergonomica = bpy.context.active_object
    objeto_silla_ergonomica.scale = (0.25, 0.25, 0.25)
    
    # Cajonera
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-3 + 1.75 * i, -2.25, 2))
    objeto_cajonera = bpy.context.active_object
    objeto_cajonera.scale = (0.5, 0.5, 0.5)

# Crea la separación entre el espacio principal y la sala de reuniones
bpy.ops.mesh.primitive_cube_add(size=1, location=(3.25, 4.25, 2))
objeto_separacion = bpy.context.active_object
objeto_separacion.scale = (0.5, 0.5, 0.5)

# Crea la mesa para reuniones en la sala de reuniones
bpy.ops.mesh.primitive_cube_add(size=1, location=(3.25, 4.25, 2))
objeto_mesa_reuniones = bpy.context.active_object
objeto_mesa_reuniones.scale = (sala_reuniones[0], 0.5, sala_reuniones[2])

# Crea las sillas para reuniones en la sala de reuniones
for i in range(6):
    # Silla
    bpy.ops.mesh.primitive_cube_add(size=0.25, location=(3.25 + (sala_reuniones[0] - 1) / 5 * (i % 2 == 0 and 1 or -1), 4.75, 2))
    objeto_silla_reunion = bpy.context.active_object
    objeto_silla_reunion.scale = (0.25, 0.25, 0.25)

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])