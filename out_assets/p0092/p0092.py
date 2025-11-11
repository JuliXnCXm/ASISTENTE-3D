import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros
longitud_cable = 1.0
radio_pantalla = 0.20 # 40cm diametro
altura_techo_virtual = 3.0

# Crear el cable (cilindro delgado)
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.005, 
    depth=longitud_cable, 
    location=(0, 0, altura_techo_virtual - longitud_cable / 2)
)
cable = bpy.context.active_object
cable.name = 'CableLampara'

# Crear la pantalla (esfera cortada)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio_pantalla, 
    location=(0, 0, altura_techo_virtual - longitud_cable)
)
pantalla = bpy.context.active_object
pantalla.name = 'PantallaLampara'

# Cortar la mitad inferior de la esfera en modo edición
bpy.ops.object.select_all(action='DESELECT')
pantalla.select_set(True)
bpy.context.view_layer.objects.active = pantalla
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bisect(plane_co=(0, 0, pantalla.location.z), plane_no=(0, 0, 1), clear_outer=True)
bpy.ops.object.editmode_toggle()

# Crear bombilla simple
bpy.ops.mesh.primitive_ico_sphere_add(
    radius=0.05, 
    location=(0, 0, altura_techo_virtual - longitud_cable - 0.05)
)
bombilla = bpy.context.active_object
bombilla.name = 'Bombilla'