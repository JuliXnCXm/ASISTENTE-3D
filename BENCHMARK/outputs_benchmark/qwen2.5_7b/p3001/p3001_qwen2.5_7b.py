import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
ancho = 5.0
largo = 10.0
altura = 3.0

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1))
suelo = bpy.context.object
suelo.scale = (ancho * 2, largo * 2, 1)

# Crear la pared frontal y trasera
for i in range(2):
    bpy.ops.mesh.primitive_cube_add(size=altura, location=(i == 0 and -largo / 2 or largo / 2, 0, altura / 2))
    pared = bpy.context.object
    pared.scale = (1 if i == 0 else 1, ancho * 2, altura)
    pared.rotation_euler[0] = 1.57

# Crear la pared lateral izquierda
bpy.ops.mesh.primitive_cube_add(size=altura, location=(-largo / 2, -ancho / 2, altura / 2))
pared_izquierda = bpy.context.object
pared_izquierda.scale = (largo, ancho * 2, altura)
pared_izquierda.rotation_euler[1] = 1.57

# Crear la pared lateral derecha
bpy.ops.mesh.primitive_cube_add(size=altura, location=(largo / 2, -ancho / 2, altura / 2))
pared_derecha = bpy.context.object
pared_derecha.scale = (largo, ancho * 2, altura)
pared_derecha.rotation_euler[1] = 1.57

# Crear el techo
bpy.ops.mesh.primitive_plane_add(size=ancho * 2 + largo * 2, location=(0, 0, altura))
techo = bpy.context.object
techo.scale = (ancho * 2 + largo * 2, ancho * 2, 1)
techo.rotation_euler[0] = -1.57

# Crear la puerta principal
bpy.ops.mesh.primitive_cube_add(size=altura / 4, location=(-largo / 2 + altura / 8, 0, altura / 2))
puerta_principal = bpy.context.object
puerta_principal.scale = (altura / 2, ancho * 2 - 1.5, altura / 2)
puerta_principal.rotation_euler[1] = 1.57

# Crear la puerta de acceso a la zona privada
bpy.ops.mesh.primitive_cube_add(size=altura / 4, location=(largo / 2 - ancho * 0.8, -ancho / 4, altura / 2))
puerta_zona_privada = bpy.context.object
puerta_zona_privada.scale = (altura / 2, ancho / 3, altura / 2)
puerta_zona_privada.rotation_euler[1] = 1.57

# Crear la ventana en la pared lateral izquierda
bpy.ops.mesh.primitive_cube_add(size=altura / 4, location=(-largo / 2 + ancho * 0.8, -ancho / 2 + altura / 6, altura / 2))
ventana_izquierda = bpy.context.object
ventana_izquierda.scale = (altura / 2, ancho / 3, altura / 2)
ventana_izquierda.rotation_euler[1] = 1.57

# Crear la ventana en la pared lateral derecha
bpy.ops.mesh.primitive_cube_add(size=altura / 4, location=(largo / 2 - ancho * 0.8, -ancho / 2 + altura / 6, altura / 2))
ventana_derecha = bpy.context.object
ventana_derecha.scale = (altura / 2, ancho / 3, altura / 2)
ventana_derecha.rotation_euler[1] = 1.57

# Crear el dormitorio principal y el baño
bpy.ops.mesh.primitive_cube_add(size=ancho * 0.8, location=(largo / 4 - ancho * 0.4, -ancho * 0.3, altura / 2))
dormitorio_principal = bpy.context.object
dormitorio_principal.scale = (ancho * 0.8, ancho * 0.6, altura)
bpy.ops.mesh.primitive_cube_add(size=ancho * 0.4, location=(largo / 4 - ancho * 0.5, -ancho * 0.3 + ancho * 0.2, altura / 2))
baño = bpy.context.object
baño.scale = (ancho * 0.4, ancho * 0.6, altura)

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)