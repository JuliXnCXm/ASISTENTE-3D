import bpy

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
tamaño_hab = 4.0
altura_techo = 2.4
ancho_foseado = 0.2
espesor_techo = 0.05

# Crear el panel central del falso techo
tamaño_panel_central = tamaño_hab - (2 * ancho_foseado)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, altura_techo))
panel_central = bpy.context.active_object
panel_central.name = 'FalsoTecho_Central'
panel_central.dimensions = (tamaño_panel_central, tamaño_panel_central, espesor_techo)

# Crear los 4 paneles perimetrales del foseado
def crear_panel_perimetral(nombre, dimensiones, posicion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=posicion)
    panel = bpy.context.active_object
    panel.name = nombre
    panel.dimensions = dimensiones

pos_perimetro = tamaño_hab/2 - ancho_foseado/2

# Norte
crear_panel_perimetral('Foseado_Norte', (tamaño_hab, ancho_foseado, espesor_techo), (0, pos_perimetro, altura_techo))
# Sur
crear_panel_perimetral('Foseado_Sur', (tamaño_hab, ancho_foseado, espesor_techo), (0, -pos_perimetro, altura_techo))
# Este
crear_panel_perimetral('Foseado_Este', (ancho_foseado, tamaño_panel_central, espesor_techo), (pos_perimetro, 0, altura_techo))
# Oeste
crear_panel_perimetral('Foseado_Oeste', (ancho_foseado, tamaño_panel_central, espesor_techo), (-pos_perimetro, 0, altura_techo))