import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

def crear_estanteria():
    alto_total = 1.8
    ancho_total = 0.8
    profundidad_total = 0.3
    espesor_panel = 0.02
    num_baldas = 5

    objetos_a_unir = []

    # Paneles laterales
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho_total / 2 + espesor_panel / 2, 0, alto_total / 2))
    panel_izq = bpy.context.active_object
    panel_izq.name = "Panel_Izquierdo"
    panel_izq.dimensions = (espesor_panel, profundidad_total, alto_total)
    objetos_a_unir.append(panel_izq)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho_total / 2 - espesor_panel / 2, 0, alto_total / 2))
    panel_der = bpy.context.active_object
    panel_der.name = "Panel_Derecho"
    panel_der.dimensions = (espesor_panel, profundidad_total, alto_total)
    objetos_a_unir.append(panel_der)

    # Baldas
    espacio_entre_baldas = alto_total / (num_baldas - 1)
    for i in range(num_baldas):
        z_pos = i * espacio_entre_baldas if i < num_baldas -1 else alto_total - espesor_panel
        if i == 0: z_pos = espesor_panel
        z_pos -= espesor_panel / 2

        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z_pos))
        balda = bpy.context.active_object
        balda.name = f"Balda_{i+1}"
        balda.dimensions = (ancho_total - 2 * espesor_panel, profundidad_total, espesor_panel)
        objetos_a_unir.append(balda)

    # Unir todas las partes
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objetos_a_unir:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objetos_a_unir[0]
    bpy.ops.object.join()
    estanteria_final = bpy.context.active_object
    estanteria_final.name = "Estanteria"
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

crear_estanteria()