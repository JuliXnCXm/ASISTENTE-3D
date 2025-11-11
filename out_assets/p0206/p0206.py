import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura_poste = 8.0
radio_poste = 0.1
longitud_brazo = 1.5
radio_brazo = 0.08

# Crear poste principal
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)

# Crear brazo curvado usando una curva Bezier
bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False, align='WORLD', location=(0, 0, altura_poste))
curva_obj = bpy.context.object
curva_obj.data.dimensions = '3D'
curva_obj.data.fill_mode = 'FULL'
curva_obj.data.bevel_depth = radio_brazo
curva_obj.data.bevel_resolution = 4

# Modificar la forma de la curva para el brazo
# Esto se hace creando una nueva curva, no en edit mode
points = [(0, 0, 0), (0, longitud_brazo * 0.5, 0), (0, longitud_brazo, -0.5)]
new_curve = bpy.data.curves.new('ArmCurve', 'CURVE')
new_curve.dimensions = '3D'
spline = new_curve.splines.new('BEZIER')
spline.bezier_points.add(len(points) - 1)
for i, p in enumerate(points):
    spline.bezier_points[i].co = p
    spline.bezier_points[i].handle_left_type = 'AUTO'
    spline.bezier_points[i].handle_right_type = 'AUTO'

bpy.data.objects.remove(curva_obj, do_unlink=True)
brazo_obj = bpy.data.objects.new('Arm', new_curve)
brazo_obj.location = (0, 0, altura_poste)
brazo_obj.data.bevel_depth = radio_brazo
scene.collection.objects.link(brazo_obj)

# Crear luminaria
luminaria_pos = brazo_obj.location + spline.bezier_points[-1].co
bpy.ops.mesh.primitive_cube_add(size=0.4, location=luminaria_pos)
luminaria = bpy.context.object
luminaria.scale = (1, 1.5, 0.5)
bpy.ops.object.transform_apply(scale=True)