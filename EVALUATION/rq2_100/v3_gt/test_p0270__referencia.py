import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configuración de escena
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_total = 6.0
alto_total = 3.0
grosor_perfil = 0.1
espesor_vidrio = 0.005
div_horizontales = 4
div_verticales = 2

# Crear un objeto contenedor
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
padre_fachada = bpy.context.object
padre_fachada.name = "FachadaMuroCortina"

# Crear perfiles verticales (montantes)
for i in range(div_verticales + 1):
    pos_x = -ancho_total / 2 + i * (ancho_total / div_verticales)
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, 0, alto_total / 2),
        scale=(grosor_perfil / 2, grosor_perfil / 2, alto_total / 2)
    )
    montante = bpy.context.object
    montante.name = f"Montante_{i+1}"
    montante.parent = padre_fachada

# Crear perfiles horizontales (travesaños)
ancho_hueco = ancho_total / div_verticales - grosor_perfil
for i in range(div_horizontales + 1):
    pos_z = i * (alto_total / div_horizontales)
    for j in range(div_verticales):
        pos_x = -ancho_total/2 + grosor_perfil/2 + j * (ancho_total/div_verticales) + ancho_hueco/2
        bpy.ops.mesh.primitive_cube_add(
            location=(pos_x, 0, pos_z),
            scale=(ancho_hueco / 2, grosor_perfil / 2, grosor_perfil / 2)
        )
        travesano = bpy.context.object
        travesano.name = f"Travesano_{i+1}_{j+1}"
        travesano.parent = padre_fachada

# Crear paneles de vidrio
alto_hueco = alto_total / div_horizontales - grosor_perfil
for i in range(div_horizontales):
    pos_z = grosor_perfil/2 + i * (alto_total/div_horizontales) + alto_hueco/2
    for j in range(div_verticales):
        pos_x = -ancho_total/2 + grosor_perfil/2 + j * (ancho_total/div_verticales) + ancho_hueco/2
        bpy.ops.mesh.primitive_cube_add(
            location=(pos_x, 0, pos_z),
            scale=(ancho_hueco / 2, espesor_vidrio / 2, alto_hueco / 2)
        )
        vidrio = bpy.context.object
        vidrio.name = f"Vidrio_{i+1}_{j+1}"
        vidrio.parent = padre_fachada