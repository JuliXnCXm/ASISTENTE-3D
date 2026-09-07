import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del edificio
ancho = 15.0  # metros
profundidad = 10.0  # metros
altura_planta = 3.0  # metros
altura_total = altura_planta * 3  # metros

# Dimensiones de la ventana
ancho_ventana = 1.0  # metros
alto_ventana = 1.2  # metros
separacion_ventana = 0.5  # metros

# Material de aluminio
material_aluminio = bpy.data.materials.new(name="Aluminio")
material_aluminio.use_nodes = True
principled_bsdf = material_aluminio.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
principled_bsdf.inputs["Metallic"].default_value = 0.9
principled_bsdf.inputs["Roughness"].default_value = 0.2


# Función para crear una pared
def crear_pared(x, y, z, ancho, alto, profundidad, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    pared = bpy.context.object
    pared.scale = (ancho / 2, profundidad / 2, alto / 2)
    pared.location = (x, y, z)
    pared.name = "Pared"
    pared.data.materials.append(material)
    return pared

# Crear base
base = crear_pared(0, 0, 0, ancho, 0.2, profundidad, material_aluminio)

# Crear paredes
pared_trasera = crear_pared(0, profundidad / 2, altura_total / 2, ancho, altura_total, 0.2, material_aluminio)
pared_frontal = crear_pared(0, -profundidad / 2, altura_total / 2, ancho, altura_total, 0.2, material_aluminio)
pared_izquierda = crear_pared(-ancho / 2, 0, altura_total / 2, 0.2, altura_total, profundidad, material_aluminio)
pared_derecha = crear_pared(ancho / 2, 0, altura_total / 2, 0.2, altura_total, profundidad, material_aluminio)

# Crear ventanas
def crear_ventana(x, y, z):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    ventana = bpy.context.object
    ventana.scale = (ancho_ventana / 2, 0.1, alto_ventana / 2)
    ventana.location = (x, y, z)
    ventana.name = "Ventana"
    ventana.data.materials.append(material_aluminio)
    return ventana

# Crear ventanas en la pared frontal
for i in range(int(ancho / (ancho_ventana + separacion_ventana))):
    x = -ancho / 2 + i * (ancho_ventana + separacion_ventana) + ancho_ventana / 2
    crear_ventana(x, -profundidad / 2 + 0.1, altura_total / 2)

# Crear ventanas en la pared trasera
for i in range(int(ancho / (ancho_ventana + separacion_ventana))):
    x = -ancho / 2 + i * (ancho_ventana + separacion_ventana) + ancho_ventana / 2
    crear_ventana(x, profundidad / 2 + 0.1, altura_total / 2)

# Crear techo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, altura_total + 0.1))
techo = bpy.context.object
techo.scale = (ancho / 2, profundidad / 2, 0.2)
techo.location = (0, 0, altura_total + 0.1)
techo.name = "Techo"
techo.data.materials.append(material_aluminio)

# Guardar la escena
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])