import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura_poste = 4.0
radio_poste = 0.07
longitud_brazo = 1.0
radio_brazo = 0.05
segmentos_curva = 12

# Crear poste principal
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = 'PosteFarola'

# Crear brazo curvado usando un objeto Curva Bezier
bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, location=(0, 0, altura_poste))
curva_obj = bpy.context.active_object
curva_obj.name = 'CurvaBrazo'

# Manipular los puntos de control de la curva para formar un arco
bpy.ops.curve.select_all(action='SELECT')
bpy.ops.transform.rotate(value=math.radians(90), orient_axis='Z')

# Acceso a los puntos de la curva
# El modo edición se activa con el operador, por lo que podemos acceder a los datos
curva_data = curva_obj.data
punto1 = curva_data.splines[0].bezier_points[0]
punto2 = curva_data.splines[0].bezier_points[1]

punto1.co = (0, 0, 0)
punto1.handle_right_type = 'FREE'
punto1.handle_right = (0, longitud_brazo / 2, 0)

punto2.co = (0, longitud_brazo, -longitud_brazo / 2)
punto2.handle_left_type = 'FREE'
punto2.handle_left = (0, longitud_brazo / 2, -longitud_brazo / 2)

bpy.ops.object.mode_set(mode='OBJECT')

# Darle grosor a la curva
curva_obj.data.dimensions = '3D'
curva_obj.data.fill_mode = 'FULL'
curva_obj.data.bevel_depth = radio_brazo
curva_obj.data.bevel_resolution = 4

# Convertir curva a malla
bpy.ops.object.convert(target='MESH')
brazo = bpy.context.active_object
brazo.name = 'BrazoFarola'

# Crear luminaria
pos_luminaria = brazo.matrix_world @ punto2.co
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.2, subdivisions=2, location=pos_luminaria)
luminaria = bpy.context.active_object
luminaria.name = 'Luminaria'
bpy.ops.transform.resize(value=(1, 1, 0.6))