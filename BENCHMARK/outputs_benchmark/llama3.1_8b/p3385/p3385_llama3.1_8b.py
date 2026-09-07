import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del apartamento
ancho = 8  # metros
largo_sala = 6  # metros
largo_cocina = 3.5  # metros
alto_pared = 2.7  # metros

# Crea la sala-comedor
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, -largo_sala/2, 0))
obj_sala = bpy.context.active_object
obj_sala.scale = (largo_sala, ancho, alto_pared)

# Crea la cocina semi-abierta
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, -largo_cocina/2, 0))
obj_cocina = bpy.context.active_object
obj_cocina.scale = (largo_cocina, ancho, alto_pared)

# Crea la barra de la cocina
bpy.ops.mesh.primitive_cube_add(size=ancho*0.5, location=(0, -largo_cocina/2 + 1, 0))
obj_barra = bpy.context.active_object
obj_barra.scale = (ancho*0.5, ancho*0.5, alto_pared)

# Crea el pasillo corto
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, -largo_sala/2 + 1, 0))
obj_pasillo = bpy.context.active_object
obj_pasillo.scale = (ancho, ancho*0.5, alto_pared)

# Crea el baño completo
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, -largo_sala/2 + 1.5, 0))
obj_baño = bpy.context.active_object
obj_baño.scale = (ancho, ancho*0.5, alto_pared)

# Crea el dormitorio doble con espacio para un armario grande
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, -largo_sala/2 + 3, 0))
obj_dormitorio = bpy.context.active_object
obj_dormitorio.scale = (ancho, ancho*1.5, alto_pared)

# Crea la ventana de la sala
bpy.ops.mesh.primitive_cube_add(size=ancho*0.5, location=(0, -largo_sala/2 + 0.5, 0))
obj_ventana_sala = bpy.context.active_object
obj_ventana_sala.scale = (ancho*0.5, ancho*0.5, alto_pared)

# Crea la ventana del dormitorio
bpy.ops.mesh.primitive_cube_add(size=ancho*0.5, location=(0, -largo_sala/2 + 3.5, 0))
obj_ventana_dormitorio = bpy.context.active_object
obj_ventana_dormitorio.scale = (ancho*0.5, ancho*0.5, alto_pared)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])