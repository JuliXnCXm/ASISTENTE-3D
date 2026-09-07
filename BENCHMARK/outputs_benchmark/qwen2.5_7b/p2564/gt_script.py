import bpy

# Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
dim_x, dim_y, dim_z = 5.0, 4.0, 2.7
espesor = 0.15

def crear_muro(nombre, loc, sca):
    bpy.ops.mesh.primitive_cube_add(location=loc, scale=sca)
    muro = bpy.context.active_object
    muro.name = nombre
    bpy.ops.object.transform_apply(scale=True)

# Suelo y Techo
crear_muro('Suelo', (dim_x/2, dim_y/2, -espesor/2), (dim_x+espesor*2, dim_y+espesor*2, espesor))
crear_muro('Techo', (dim_x/2, dim_y/2, dim_z+espesor/2), (dim_x+espesor*2, dim_y+espesor*2, espesor))

# Muros
crear_muro('Muro_Norte', (dim_x/2, dim_y+espesor/2, dim_z/2), (dim_x, espesor, dim_z))
crear_muro('Muro_Sur', (dim_x/2, -espesor/2, dim_z/2), (dim_x, espesor, dim_z))
crear_muro('Muro_Este', (dim_x+espesor/2, dim_y/2, dim_z/2), (espesor, dim_y, dim_z))
crear_muro('Muro_Oeste', (-espesor/2, dim_y/2, dim_z/2), (espesor, dim_y, dim_z))

# Mobiliario
# Cama (base + colchón)
cama_l, cama_a, cama_h = 1.9, 1.4, 0.2
pos_cama_x = dim_x / 2
pos_cama_y = dim_y - cama_a/2 - 0.1 # 10cm de la pared norte
crear_muro('Base_Cama', (pos_cama_x, pos_cama_y, cama_h/2), (cama_l, cama_a, cama_h))
crear_muro('Colchon', (pos_cama_x, pos_cama_y, cama_h + cama_h/2), (cama_l, cama_a, cama_h))

# Mesa de noche
mesa_dim = 0.4
mesa_h = 0.5
pos_mesa_x = pos_cama_x - cama_l/2 - mesa_dim/2 - 0.1 # 10cm de la cama
pos_mesa_y = dim_y - mesa_dim/2 - 0.1 # 10cm de la pared
crear_muro('Mesa_Noche', (pos_mesa_x, pos_mesa_y, mesa_h/2), (mesa_dim, mesa_dim, mesa_h))