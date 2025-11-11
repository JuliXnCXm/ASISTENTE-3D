import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Dimensiones
ancho_int_x = 4.0
prof_int_y = 5.0
altura_z = 2.8
espesor_muro = 0.2

# Crear piso como referencia (opcional)
bpy.ops.mesh.primitive_plane_add(size=1, location=(ancho_int_x/2, prof_int_y/2, 0))
piso_ref = bpy.context.active_object
piso_ref.dimensions = (ancho_int_x, prof_int_y, 0)

# Muros
def crear_muro(nombre, loc, escala):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    muro = bpy.context.active_object
    muro.name = nombre
    muro.scale = escala
    bpy.ops.object.transform_apply(scale=True, location=False, rotation=False)

# Muro Norte
loc_n = (ancho_int_x / 2, prof_int_y + espesor_muro / 2, altura_z / 2)
esc_n = (ancho_int_x / 2 + espesor_muro, espesor_muro / 2, altura_z / 2)
crear_muro("MuroNorte", loc_n, esc_n)

# Muro Sur
loc_s = (ancho_int_x / 2, -espesor_muro / 2, altura_z / 2)
esc_s = (ancho_int_x / 2 + espesor_muro, espesor_muro / 2, altura_z / 2)
crear_muro("MuroSur", loc_s, esc_s)

# Muro Este
loc_e = (ancho_int_x + espesor_muro / 2, prof_int_y / 2, altura_z / 2)
esc_e = (espesor_muro / 2, prof_int_y / 2, altura_z / 2)
crear_muro("MuroEste", loc_e, esc_e)

# Muro Oeste
loc_o = (-espesor_muro / 2, prof_int_y / 2, altura_z / 2)
esc_o = (espesor_muro / 2, prof_int_y / 2, altura_z / 2)
crear_muro("MuroOeste", loc_o, esc_o)