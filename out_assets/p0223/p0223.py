import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Poste
altura_poste = 4.0
diametro_poste = 0.15
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_poste / 2,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "PosteFarola"

# Brazo curvo (usando una curva Bezier)
bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False, align='WORLD', location=(0,0,0))
brazo_curva = bpy.context.active_object
brazo_curva.name = "BrazoCurvo"
brazo_curva.data.dimensions = '3D'
brazo_curva.data.fill_mode = 'FULL'
brazo_curva.data.bevel_depth = 0.04
brazo_curva.data.bevel_resolution = 4

# Modificar puntos de la curva
# Punto 1: Conexión con el poste
brazo_curva.data.splines[0].bezier_points[0].co = (0, 0, altura_poste - 0.2)
brazo_curva.data.splines[0].bezier_points[0].handle_left_type = 'AUTO'
brazo_curva.data.splines[0].bezier_points[0].handle_right_type = 'ALIGNED'
brazo_curva.data.splines[0].bezier_points[0].handle_right = (0, 0.3, altura_poste - 0.2)

# Punto 2: Extremo de la luminaria
brazo_curva.data.splines[0].bezier_points[1].co = (0, 0.6, altura_poste)
brazo_curva.data.splines[0].bezier_points[1].handle_left_type = 'AUTO'
brazo_curva.data.splines[0].bezier_points[1].handle_right_type = 'AUTO'
brazo_curva.data.splines[0].bezier_points[1].handle_left = (0, 0.3, altura_poste)

# Luminaria
largo_lum = 0.5
ancho_lum = 0.3
alto_lum = 0.1
bpy.ops.mesh.primitive_cube_add(location=(0, 0.6 + largo_lum/2 - 0.1, altura_poste))
luminaria = bpy.context.active_object
luminaria.name = "CabezaLuminaria"
luminaria.dimensions = (ancho_lum, largo_lum, alto_lum)

# Fuente de luz
bpy.ops.object.light_add(type='AREA', location=(0, 0.6 + largo_lum/2 - 0.1, altura_poste - alto_lum/2))
luz = bpy.context.active_object
luz.data.size = ancho_lum
luz.data.size_y = largo_lum
luz.data.energy = 150 # Watts
luz.rotation_euler[0] = 1.5708 # 90 grados en radianes para apuntar hacia abajo