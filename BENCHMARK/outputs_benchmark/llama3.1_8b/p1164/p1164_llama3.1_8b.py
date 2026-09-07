import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del dormitorio
ancho = 4
alto = 5

# Crea el piso de parquet
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
piso = bpy.context.active_object
piso.scale = (ancho, alto, 0.01)
piso.name = 'Piso'

# Crea la pared del fondo
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -alto))
pared_fondo = bpy.context.active_object
pared_fondo.scale = (ancho, alto, alto)
pared_fondo.name = 'Pared Fondo'

# Crea la pared del lado izquierdo
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -alto))
pared_izquierda = bpy.context.active_object
pared_izquierda.scale = (ancho, alto, alto)
pared_izquierda.name = 'Pared Izquierda'

# Crea la pared del lado derecho
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -alto))
pared_derecha = bpy.context.active_object
pared_derecha.scale = (ancho, alto, alto)
pared_derecha.name = 'Pared Derecha'

# Crea la pared de la esquina superior izquierda
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -alto))
pared_esquina_superior_izquierda = bpy.context.active_object
pared_esquina_superior_izquierda.scale = (ancho/2, alto/2, alto)
pared_esquina_superior_izquierda.name = 'Pared Esquina Superior Izquierda'

# Crea la pared de la esquina superior derecha
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -alto))
pared_esquina_superior_derecha = bpy.context.active_object
pared_esquina_superior_derecha.scale = (ancho/2, alto/2, alto)
pared_esquina_superior_derecha.name = 'Pared Esquina Superior Derecha'

# Crea la pared de la esquina inferior izquierda
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -alto))
pared_esquina_inferior_izquierda = bpy.context.active_object
pared_esquina_inferior_izquierda.scale = (ancho/2, alto/2, alto)
pared_esquina_inferior_izquierda.name = 'Pared Esquina Inferior Izquierda'

# Crea la pared de la esquina inferior derecha
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -alto))
pared_esquina_inferior_derecha = bpy.context.active_object
pared_esquina_inferior_derecha.scale = (ancho/2, alto/2, alto)
pared_esquina_inferior_derecha.name = 'Pared Esquina Inferior Derecha'

# Crea la cama de matrimonio
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(ancho/2 - 0.5, alto/2 - 0.5, -alto))
cama = bpy.context.active_object
cama.scale = (1, 1.8, 0.01)
cama.name = 'Cama'

# Crea el armario
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(ancho/4 - 0.5, alto/2 - 0.5, -alto))
armario = bpy.context.active_object
armario.scale = (0.8, 1.5, 0.01)
armario.name = 'Armario'

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])