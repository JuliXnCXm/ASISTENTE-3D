import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros
altura = 2.5
espesor = 0.15
largo_trasero = 4.0
largo_lateral = 3.0

def crear_muro(nombre, escala, posicion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=posicion, scale=escala)
    muro = bpy.context.active_object
    muro.name = nombre

# Muro Trasero (Norte)
escala_trasero = (largo_trasero, espesor, altura)
pos_trasero = (0, largo_lateral / 2 - espesor / 2, altura / 2)
crear_muro('MuroTrasero', escala_trasero, pos_trasero)

# Muro Lateral (Oeste)
escala_lateral_1 = (espesor, largo_lateral, altura)
pos_lateral_1 = (-largo_trasero / 2 + espesor / 2, 0, altura / 2)
crear_muro('MuroOeste', escala_lateral_1, pos_lateral_1)

# Muro Lateral (Este)
escala_lateral_2 = (espesor, largo_lateral, altura)
pos_lateral_2 = (largo_trasero / 2 - espesor / 2, 0, altura / 2)
crear_muro('MuroEste', escala_lateral_2, pos_lateral_2)