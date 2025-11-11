import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de los muros ---
altura = 2.8
espesor = 0.3
largo_trasero = 8.0
largo_lateral = 6.0

# --- Creación del muro trasero (a lo largo del eje X) ---
pos_x_trasero = 0
pos_y_trasero = -largo_lateral / 2 + espesor / 2
pos_z = altura / 2
bpy.ops.mesh.primitive_cube_add(
    location=(pos_x_trasero, pos_y_trasero, pos_z)
)
muro_trasero = bpy.context.active_object
muro_trasero.name = "MuroTrasero"
muro_trasero.dimensions = (largo_trasero, espesor, altura)

# --- Creación del muro lateral izquierdo ---
pos_x_izq = -largo_trasero / 2 + espesor / 2
pos_y_izq = 0
bpy.ops.mesh.primitive_cube_add(
    location=(pos_x_izq, pos_y_izq, pos_z)
)
muro_izq = bpy.context.active_object
muro_izq.name = "MuroLateralIzquierdo"
muro_izq.dimensions = (espesor, largo_lateral, altura)

# --- Creación del muro lateral derecho ---
pos_x_der = largo_trasero / 2 - espesor / 2
pos_y_der = 0
bpy.ops.mesh.primitive_cube_add(
    location=(pos_x_der, pos_y_der, pos_z)
)
muro_der = bpy.context.active_object
muro_der.name = "MuroLateralDerecho"
muro_der.dimensions = (espesor, largo_lateral, altura)