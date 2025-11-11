import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones y posiciones
altura_suelo = 2.2
longitud_cable = 1.0
radio_bombilla = 0.05
altura_casquillo = 0.08
radio_casquillo = 0.03
radio_cable = 0.005

# Posición Z de los elementos
z_bombilla = altura_suelo
z_casquillo = z_bombilla + radio_bombilla
z_cable = z_casquillo + altura_casquillo / 2

# Crear bombilla
bpy.ops.mesh.primitive_uv_sphere_add(radius=radio_bombilla, location=(0, 0, z_bombilla))
bombilla = bpy.context.active_object
bombilla.name = 'Bombilla'
bpy.ops.object.shade_smooth()

# Crear casquillo
bpy.ops.mesh.primitive_cylinder_add(radius=radio_casquillo, depth=altura_casquillo, location=(0, 0, z_casquillo))
casquillo = bpy.context.active_object
casquillo.name = 'Casquillo'

# Crear cable
bpy.ops.mesh.primitive_cylinder_add(radius=radio_cable, depth=longitud_cable, location=(0, 0, z_cable + longitud_cable/2 - altura_casquillo/2))
cable = bpy.context.active_object
cable.name = 'Cable'