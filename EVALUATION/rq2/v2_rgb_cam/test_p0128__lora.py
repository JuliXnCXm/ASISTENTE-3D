import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

def crear_estanteria():
    # Dimensiones
    alto_total = 1.8
    ancho_total = 0.8
    prof_total = 0.3
    num_estantes = 5
    espesor_panel = 0.02
    grosor_poste = 0.02

    # Crear postes verticales
    pos_x = ancho_total / 2 - grosor_poste / 2
    pos_y = prof_total / 2 - grosor_poste / 2
    for i in range(2):
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(pos_x if i == 0 else -pos_x, pos_y, alto_total / 2),
            scale=(grosor_poste, grosor_poste, alto_total)
        )
        bpy.context.object.name = f"Poste_{i}"

    # Crear estantes horizontales
    altura_estante = alto_total / (num_estantes + 1)
    for i in range(num_estantes):
        z_pos = altura_estante * (i + 1) - altura_estante / 2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(0, 0, z_pos),
            scale=(ancho_total - 2 * grosor_poste, prof_total, espesor_panel)
        )
        bpy.context.object.name = f"Estante_{i+1}"

crear_estanteria()