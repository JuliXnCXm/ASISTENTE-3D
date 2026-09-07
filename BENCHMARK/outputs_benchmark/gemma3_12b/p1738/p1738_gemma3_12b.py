import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Configuración ---
radio_copa = 2.0  # Radio de la copa en metros
altura_copa = 4.0  # Altura de la copa en metros
altura_tronco = 2.5  # Altura del tronco en metros
segmentos_circulo = 32  # Número de segmentos para la copa

# --- Crear el tronco ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.3,
    depth=altura_tronco,
    vertices=16,
    location=(0, 0, altura_tronco / 2)
)
tronco = bpy.context.object
tronco.name = "Tronco"

# --- Crear la copa ---
bpy.ops.mesh.primitive_circle_add(
    radius=radio_copa,
    vertices=segmentos_circulo,
    location=(0, 0, altura_copa)
)
copa = bpy.context.object
copa.name = "Copa"

# Extruir la copa para darle altura
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -altura_copa)})
bpy.ops.object.mode_set(mode='OBJECT')

# Escalar la copa para darle forma
copa.scale = (1, 1, 1)

# --- Unir el tronco y la copa ---
# Posicionar la copa para que se conecte al tronco
copa.location = (0, 0, altura_copa)

# Unir los objetos
bpy.context.view_layer.objects.active = tronco
tronco.select_set(True)
copa.select_set(True)
bpy.ops.object.join()

# Renombrar el objeto combinado
arbol = bpy.context.object
arbol.name = "Arbol"

# --- Opcional: Guardar el archivo ---
if "BLEND_OUT" in os.environ:
    arbol.save_blend(os.environ["BLEND_OUT"])