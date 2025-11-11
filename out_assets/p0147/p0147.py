import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Dimensiones generales
alto_total = 1.8
ancho_total = 1.0
fondo_total = 0.3
espesor_madera = 0.02
numero_estantes = 5

# Crear paneles laterales
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * (ancho_total / 2 - espesor_madera / 2), fondo_total / 2, alto_total / 2)
    )
    panel = bpy.context.active_object
    panel.dimensions = (espesor_madera, fondo_total, alto_total)
    bpy.ops.object.transform_apply(scale=True)

# Crear estantes
espacio_entre_estantes = alto_total / (numero_estantes - 1)
ancho_estante = ancho_total - 2 * espesor_madera

for i in range(numero_estantes):
    altura_estante = i * espacio_entre_estantes if numero_estantes > 1 else alto_total / 2
    # Asegurar que el primer estante esté en z=0 y el último en z=alto_total-espesor
    if i == 0:
        z_pos = espesor_madera / 2
    elif i == numero_estantes - 1:
        z_pos = alto_total - espesor_madera / 2
    else:
        z_pos = (alto_total / (numero_estantes -1)) * i

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, fondo_total / 2, z_pos)
    )
    estante = bpy.context.active_object
    estante.dimensions = (ancho_estante, fondo_total, espesor_madera)
    bpy.ops.object.transform_apply(scale=True)