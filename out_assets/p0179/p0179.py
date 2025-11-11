import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros de la fachada
ancho_total = 10.0
alto_total = 6.0
div_h = 5 # Divisiones horizontales (filas)
div_v = 10 # Divisiones verticales (columnas)
grosor_perfil = 0.05
grosor_vidrio = 0.01

# Cálculo de dimensiones de módulo
ancho_modulo = ancho_total / div_v
alto_modulo = alto_total / div_h

# Crear colecciones para organizar
coll_montantes = bpy.data.collections.new("Montantes")
bpy.context.scene.collection.children.link(coll_montantes)
coll_travesanos = bpy.data.collections.new("Travesaños")
bpy.context.scene.collection.children.link(coll_travesanos)
coll_vidrios = bpy.data.collections.new("Vidrios")
bpy.context.scene.collection.children.link(coll_vidrios)

# Crear montantes (verticales)
for i in range(div_v + 1):
    pos_x = -ancho_total / 2 + i * ancho_modulo
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(grosor_perfil, grosor_perfil, alto_total)
    )
    obj = bpy.context.active_object
    obj.name = f"Montante_{i}"
    coll_montantes.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)

# Crear travesaños (horizontales)
for i in range(div_h + 1):
    pos_z = i * alto_modulo
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, pos_z),
        scale=(ancho_total, grosor_perfil, grosor_perfil)
    )
    obj = bpy.context.active_object
    obj.name = f"Travesaño_{i}"
    coll_travesanos.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)

# Crear paneles de vidrio
ancho_vidrio = ancho_modulo - grosor_perfil
alto_vidrio = alto_modulo - grosor_perfil

for i in range(div_v):
    for j in range(div_h):
        pos_x = -ancho_total/2 + ancho_modulo/2 + i * ancho_modulo
        pos_z = alto_modulo/2 + j * alto_modulo
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(pos_x, 0, pos_z),
            scale=(ancho_vidrio, grosor_vidrio, alto_vidrio)
        )
        obj = bpy.context.active_object
        obj.name = f"Vidrio_{i}_{j}"
        coll_vidrios.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)