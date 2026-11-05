import blender_arch as A
import bpy
import bmesh

A.limpiar_escena()

# 1. Base del jardín y columnas de la pérgola
terreno = A.crear_terreno_plano('TerrenoJardin', ancho=8, fondo=8, espesor=0.2, origen=(-4, -4, -0.2), material='Cesped')

ancho_pergola = 4.0
fondo_pergola = 3.0
alto_pergola = 2.5

for i, (x, y) in enumerate([(-ancho_pergola/2, -fondo_pergola/2), (ancho_pergola/2, -fondo_pergola/2), (-ancho_pergola/2, fondo_pergola/2), (ancho_pergola/2, fondo_pergola/2)]):
    A.crear_columna(f'Poste_{i}', seccion='rect', ancho=0.15, fondo=0.15, alto=alto_pergola, origen=(x, y, 0), material='Madera_Roble')

# 2. Viga principal personalizada con bpy
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_pergola + 0.075))
viga = bpy.context.active_object
viga.name = 'Viga_Maestra'
viga.dimensions = (ancho_pergola + 0.4, 0.15, 0.15)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Biselar extremos de la viga
bm = bmesh.new()
bm.from_mesh(viga.data)

edges_to_bevel = [e for e in bm.edges if abs(e.verts[0].co.x) > ancho_pergola/2 and abs(e.verts[0].co.y) < 0.07 and abs(e.verts[0].co.z) > 0.07]
bmesh.ops.bevel(bm, geom=edges_to_bevel, offset=0.07, segments=2)

bm.to_mesh(viga.data)
bm.free()
viga.data.update()

# Duplicar viga
viga_2 = viga.copy()
viga_2.data = viga.data.copy()
viga_2.location.y = fondo_pergola / 2
viga.location.y = -fondo_pergola / 2
bpy.context.collection.objects.link(viga_2)
A.asignar_material(viga, 'Madera_Roble')
A.asignar_material(viga_2, 'Madera_Roble')

# 3. Celosía superior con modificadores
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, alto_pergola + 0.15 + 0.03))
celosia_plano = bpy.context.active_object
celosia_plano.name = 'Base_Celosia'
celosia_plano.scale = (ancho_pergola, fondo_pergola, 1)

# Modificador Array para crear la grilla
array_mod = celosia_plano.modifiers.new(name='ArrayGrid', type='ARRAY')
array_mod.count = 10
array_mod.relative_offset_displace[0] = 0
array_mod.relative_offset_displace[1] = 1.0

# Modificador Wireframe para convertir en estructura
wire_mod = celosia_plano.modifiers.new(name='Wireframe', type='WIREFRAME')
wire_mod.thickness = 0.05
A.asignar_material(celosia_plano, 'Marco_Negro')

# 4. Simulación de vegetación
for i in range(15):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=( (i % 5 - 2) * 0.8, (i // 5 - 1) * 1.2, alto_pergola + 0.4 ))
    esfera = bpy.context.active_object
    esfera.name = f'Planta_{i}'
    esfera.modifiers.new(name='Displace', type='DISPLACE')
    A.asignar_material(esfera, base_color=(0.1, 0.5, 0.1, 1), nombre='Verde_Planta')