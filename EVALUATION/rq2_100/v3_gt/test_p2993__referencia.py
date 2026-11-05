import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Losa base de la plaza
dimension_plaza = 15.0
espesor_losa = 0.2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -espesor_losa / 2),
    scale=(dimension_plaza, dimension_plaza, espesor_losa)
)
plaza_losa = bpy.context.active_object
plaza_losa.name = 'Plaza_Losa'
bpy.ops.object.transform_apply(scale=True)

# Banco central
largo_banco = 3.0
ancho_banco = 0.5
alto_asiento = 0.45
espesor_asiento = 0.1
dim_pata = 0.1

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_asiento - espesor_asiento / 2),
    scale=(largo_banco, ancho_banco, espesor_asiento)
)
banco_asiento = bpy.context.active_object
banco_asiento.name = 'Banco_Asiento'
bpy.ops.object.transform_apply(scale=True)

for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(
            i * (largo_banco / 2 - dim_pata * 2),
            0,
            (alto_asiento - espesor_asiento) / 2
        ),
        scale=(dim_pata, ancho_banco * 0.9, alto_asiento - espesor_asiento)
    )
    pata = bpy.context.active_object
    pata.name = f'Banco_Pata_{1 if i == -1 else 2}'
    bpy.ops.object.transform_apply(scale=True)

# Árboles en las esquinas
def crear_arbol(nombre, ubicacion):
    radio_tronco = 0.15
    altura_tronco = 2.5
    radio_copa = 1.8
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radio_tronco,
        depth=altura_tronco,
        location=(ubicacion[0], ubicacion[1], altura_tronco / 2)
    )
    tronco = bpy.context.active_object
    tronco.name = f'{nombre}_Tronco'
    
    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=radio_copa,
        subdivisions=2,
        location=(ubicacion[0], ubicacion[1], altura_tronco + radio_copa * 0.8)
    )
    copa = bpy.context.active_object
    copa.name = f'{nombre}_Copa'

dist_arbol = dimension_plaza / 2 - 2.0
posiciones_arboles = [
    (dist_arbol, dist_arbol),
    (-dist_arbol, dist_arbol),
    (dist_arbol, -dist_arbol),
    (-dist_arbol, -dist_arbol)
]

for i, pos in enumerate(posiciones_arboles):
    crear_arbol(f'Arbol_{i+1}', pos)