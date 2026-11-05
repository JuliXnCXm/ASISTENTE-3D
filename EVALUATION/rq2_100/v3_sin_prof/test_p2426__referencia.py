import bpy

# --- Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Dimensiones
ancho = 0.8
alto = 1.8
profundidad = 0.3
espesor_panel = 0.02
numero_baldas = 4

# --- Creación de la estructura
# Panel izquierdo
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2 + espesor_panel/2, 0, alto/2))
pared_izquierda = bpy.context.active_object
pared_izquierda.scale = (espesor_panel, profundidad, alto)

# Panel derecho
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2 - espesor_panel/2, 0, alto/2))
pared_derecha = bpy.context.active_object
pared_derecha.scale = (espesor_panel, profundidad, alto)

# Panel superior
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto - espesor_panel/2))
panel_superior = bpy.context.active_object
panel_superior.scale = (ancho, profundidad, espesor_panel)

# Panel inferior
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, espesor_panel/2))
panel_inferior = bpy.context.active_object
panel_inferior.scale = (ancho, profundidad, espesor_panel)

# --- Creación de las baldas
ancho_interior = ancho - 2 * espesor_panel
espacio_entre_baldas = (alto - 2 * espesor_panel) / (numero_baldas + 1)

for i in range(numero_baldas):
    altura_balda = (i + 1) * espacio_entre_baldas + espesor_panel
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, altura_balda))
    balda = bpy.context.active_object
    balda.scale = (ancho_interior, profundidad, espesor_panel)

# --- Nomenclatura
bpy.context.view_layer.objects.active = pared_izquierda
estanteria_partes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in estanteria_partes:
    obj.select_set(True)
bpy.ops.object.join()
estanteria = bpy.context.active_object
estanteria.name = 'Estanteria'