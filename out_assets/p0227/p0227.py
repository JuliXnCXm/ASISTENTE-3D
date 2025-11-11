import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho_total = 6.0
alto_total = 8.0

# Dimensiones de la retícula
mod_x = 1.5
mod_y = 2.0 # En Blender, el alto es en Z

# Dimensiones de la perfilería y vidrio
grosor_perfil = 0.08
profundidad_perfil = 0.10
grosor_vidrio = 0.02

# Número de módulos
num_x = int(ancho_total / mod_x)
num_y = int(alto_total / mod_y)

# Crear Montantes (verticales)
for i in range(num_x + 1):
    loc_x = i * mod_x - ancho_total / 2
    bpy.ops.mesh.primitive_cube_add(location=(loc_x, 0, alto_total / 2))
    montante = bpy.context.active_object
    montante.name = f"Montante.{i+1:03d}"
    montante.dimensions = (grosor_perfil, profundidad_perfil, alto_total)

# Crear Travesaños (horizontales)
for i in range(num_y + 1):
    loc_z = i * mod_y
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, loc_z))
    travesano = bpy.context.active_object
    travesano.name = f"Travesano.{i+1:03d}"
    travesano.dimensions = (ancho_total + grosor_perfil, profundidad_perfil, grosor_perfil)

# Crear Paneles de Vidrio
for i in range(num_x):
    for j in range(num_y):
        loc_x = i * mod_x - ancho_total / 2 + mod_x / 2
        loc_z = j * mod_y + mod_y / 2
        bpy.ops.mesh.primitive_cube_add(location=(loc_x, 0, loc_z))
        panel = bpy.context.active_object
        panel.name = f"Vidrio.{i+1:02d}-{j+1:02d}"
        panel.dimensions = (mod_x - grosor_perfil, grosor_vidrio, mod_y - grosor_perfil)