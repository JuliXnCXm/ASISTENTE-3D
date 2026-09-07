import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Parámetros ---
altura_planta = 3.0  # metros
ancho_edificio = 15.0  # metros
profundidad_edificio = 10.0  # metros
num_plantas = 5
altura_base_asfalto = 0.2  # metros
ancho_columna = 0.5  # metros
separacion_columnas = 3.0  # metros
grosor_fachada = 0.1  # metros

# --- Funciones ---

def crear_base_asfalto(ancho, profundidad, altura):
    bpy.ops.mesh.primitive_plane_add(size=ancho, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    base = bpy.context.object
    base.scale = (1, profundidad/ancho, 1)
    base.location = (0, 0, altura)
    base.name = "Base_Asfalto"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return base

def crear_planta(ancho, profundidad, altura, grosor_fachada):
    bpy.ops.mesh.primitive_plane_add(size=ancho, enter_editmode=False, align='WORLD', location=(0, 0, altura))
    planta = bpy.context.object
    planta.scale = (1, profundidad/ancho, 1)
    planta.location = (0, 0, altura)
    planta.name = "Planta"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Extruir para darle grosor
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, grosor_fachada)})
    bpy.ops.object.mode_set(mode='OBJECT')

    return planta

def crear_columna(x, y, z, ancho, alto):
    bpy.ops.mesh.primitive_cylinder_add(radius=ancho/2, depth=alto, enter_editmode=False, align='WORLD', location=(x, y, z))
    columna = bpy.context.object
    columna.name = "Columna"
    return columna

def crear_ventana(x, y, z, ancho, alto, profundidad):
    bpy.ops.mesh.primitive_plane_add(size=ancho, enter_editmode=False, align='WORLD', location=(x, y, z))
    ventana = bpy.context.object
    ventana.scale = (1, profundidad/ancho, 1)
    ventana.location = (x, y, z)
    ventana.name = "Ventana"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ventana

# --- Creación de la escena ---

# Base de asfalto
base_asfalto = crear_base_asfalto(ancho_edificio, profundidad_edificio, altura_base_asfalto)

# Plantas
plantas = []
for i in range(num_plantas):
    altura_planta_actual = (i + 1) * altura_planta
    planta = crear_planta(ancho_edificio, profundidad_edificio, altura_planta_actual, grosor_fachada)
    plantas.append(planta)

# Columnas
columnas = []
for i in range(int(ancho_edificio / separacion_columnas) + 1):
    for j in range(int(profundidad_edificio / separacion_columnas) + 1):
        x = (i * separacion_columnas) - (ancho_edificio / 2) + (separacion_columnas/2)
        y = (j * separacion_columnas) - (profundidad_edificio / 2) + (separacion_columnas/2)
        z = altura_base_asfalto
        columna = crear_columna(x, y, z, ancho_columna, altura_planta * num_plantas)
        columnas.append(columna)

# Ventanas (solo en la fachada principal)
ventanas = []
for i in range(int(ancho_edificio / separacion_columnas) + 1):
    x = (i * separacion_columnas) - (ancho_edificio / 2) + (separacion_columnas/2)
    z = altura_base_asfalto + altura_planta
    for j in range(num_plantas):
        ventana_z = altura_base_asfalto + (j + 1) * altura_planta
        ventana = crear_ventana(x, -profundidad_edificio/2 + 0.1, ventana_z, 1.5, 0.1, 0.01)
        ventanas.append(ventana)

# --- Opcional: Guardar la escena ---
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])