import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

diametro_pantalla = 0.40
longitud_cable = 0.80
radio_cable = 0.005
altura_techo = 2.8

radio_pantalla = diametro_pantalla / 2

# Pantalla: esfera completa
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio_pantalla,
    location=(0, 0, altura_techo - longitud_cable - radio_pantalla),
    segments=48,
    ring_count=24
)
pantalla = bpy.context.active_object
pantalla.name = 'PantallaLampara'

# Cortar con booleana para obtener semiesfera (INTERSECT con caja superior)
zcut = pantalla.location.z
bpy.ops.mesh.primitive_cube_add(location=(0, 0, zcut + radio_pantalla/2))
cortador = bpy.context.active_object
cortador.name = 'CorteHemiBox'
# Dimensiones grandes en X/Y y altura = radio para conservar media esfera superior
cortador.dimensions = (diametro_pantalla * 4, diametro_pantalla * 4, radio_pantalla)

mod = pantalla.modifiers.new(name='CorteHemi', type='BOOLEAN')
mod.object = cortador
mod.operation = 'INTERSECT'

bpy.context.view_layer.objects.active = pantalla
bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.data.objects.remove(cortador, do_unlink=True)

# Grosor de la pantalla
solid = pantalla.modifiers.new(name='Grosor', type='SOLIDIFY')
solid.thickness = 0.005

# Cable
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_cable,
    depth=longitud_cable,
    location=(0, 0, altura_techo - (longitud_cable / 2)),
    vertices=24
)
cable = bpy.context.active_object
cable.name = 'CableLampara'
