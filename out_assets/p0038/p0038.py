import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_techo = 5.0
ancho_techo = 3.0
altura_principal = 3.0
suspension = 0.3
grosor_falso_techo = 0.1

# Focos
filas_focos = 2
columnas_focos = 3
radio_foco = 0.05
profundidad_foco = 0.08

# Crear falso techo
altura_falso_techo = altura_principal - suspension
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_falso_techo - grosor_falso_techo / 2),
    scale=(largo_techo, ancho_techo, grosor_falso_techo)
)
falso_techo = bpy.context.active_object
falso_techo.name = "FalsoTecho"

# Crear y distribuir focos
step_x = largo_techo / columnas_focos
step_y = ancho_techo / filas_focos

for i in range(columnas_focos):
    for j in range(filas_focos):
        x_pos = -largo_techo / 2 + step_x * (i + 0.5)
        y_pos = -ancho_techo / 2 + step_y * (j + 0.5)
        z_pos = altura_falso_techo - grosor_falso_techo
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radio_foco,
            depth=profundidad_foco,
            location=(x_pos, y_pos, z_pos)
        )
        foco = bpy.context.active_object
        foco.name = f"Foco_{i}_{j}"
        
        # Operación booleana para empotrar
        bool_mod = falso_techo.modifiers.new(name=f'FocoBooleano_{i}_{j}', type='BOOLEAN')
        bool_mod.object = foco
        bool_mod.operation = 'DIFFERENCE'
        bpy.context.view_layer.objects.active = falso_techo
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)
        bpy.data.objects.remove(foco, do_unlink=True)