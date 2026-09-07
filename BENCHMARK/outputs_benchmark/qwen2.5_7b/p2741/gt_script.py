import bpy

# Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la pérgola
ancho_total = 4.0
profundidad_total = 3.0
altura_total = 2.5
grosor_poste = 0.15
grosor_viga = 0.2

# Crear colección para organizar
coleccion_pergola = bpy.data.collections.new('Pergola')
bpy.context.scene.collection.children.link(coleccion_pergola)

# Crear los 4 postes
posiciones_postes = [
    (ancho_total/2 - grosor_poste/2, profundidad_total/2 - grosor_poste/2),
    (-ancho_total/2 + grosor_poste/2, profundidad_total/2 - grosor_poste/2),
    (-ancho_total/2 + grosor_poste/2, -profundidad_total/2 + grosor_poste/2),
    (ancho_total/2 - grosor_poste/2, -profundidad_total/2 + grosor_poste/2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pos[0], pos[1], altura_total/2))
    poste = bpy.context.active_object
    poste.name = f'Poste_{i+1}'
    poste.scale = (grosor_poste, grosor_poste, altura_total)
    coleccion_pergola.objects.link(poste)
    bpy.context.collection.objects.unlink(poste)

# Crear vigas principales (largueros)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, profundidad_total/2 - grosor_poste/2, altura_total - grosor_viga/2))
viga1 = bpy.context.active_object
viga1.name = 'Viga_Principal_1'
viga1.scale = (ancho_total, grosor_poste, grosor_viga)
coleccion_pergola.objects.link(viga1)
bpy.context.collection.objects.unlink(viga1)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -profundidad_total/2 + grosor_poste/2, altura_total - grosor_viga/2))
viga2 = bpy.context.active_object
viga2.name = 'Viga_Principal_2'
viga2.scale = (ancho_total, grosor_poste, grosor_viga)
coleccion_pergola.objects.link(viga2)
bpy.context.collection.objects.unlink(viga2)

# Crear viguetas transversales
num_viguetas = 7
for i in range(num_viguetas):
    x_pos = -ancho_total/2 + (i * ancho_total / (num_viguetas - 1))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, 0, altura_total + grosor_viga/2))
    vigueta = bpy.context.active_object
    vigueta.name = f'Vigueta_{i+1}'
    vigueta.scale = (grosor_poste, profundidad_total, grosor_viga)
    coleccion_pergola.objects.link(vigueta)
    bpy.context.collection.objects.unlink(vigueta)