import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la base
base_width = 8
base_length = 12
roof_height = 3
roof_thickness = 0.25

# Calcular la mitad del ancho de la base
half_width = base_width / 2

# Calcular la pendiente del techo
slope = roof_height / half_width

# Crear la geometría de la cubierta
def create_roof_segment(start_x, end_x, width, height, thickness):
    """Crea un segmento de la cubierta a dos aguas."""
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    roof_segment = bpy.context.object
    roof_segment.name = "RoofSegment"
    roof_segment.scale = (width / 2, 1, thickness / 2)
    bpy.ops.transform.resize(value=(1, 1, 1))
    roof_segment.location = ( (start_x + end_x) / 2, 0, height )
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    return roof_segment

# Crear los segmentos de la cubierta
roof_segment_1 = create_roof_segment(-base_length / 2, 0, base_length / 2, base_length, roof_height, roof_thickness)
roof_segment_2 = create_roof_segment(0, base_length / 2, base_length / 2, base_length, roof_height, roof_thickness)

# Unir los segmentos
bpy.ops.object.select_all(action='DESELECT')
roof_segment_1.select_set(True)
roof_segment_2.select_set(True)
bpy.context.view_layer.objects.active = roof_segment_1
bpy.ops.object.join()

# Renombrar el objeto combinado
roof_object = bpy.context.object
roof_object.name = "Roof"

# Aplicar modificador solidify
bpy.ops.object.modifier_add(type='SOLIDIFY')
roof_object.modifiers["Solidify"].thickness = roof_thickness
bpy.ops.object.modifier_apply(modifier="Solidify")

# Centrar la cubierta
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center=True)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)