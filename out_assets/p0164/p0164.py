import bpy
import bmesh

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
largo = 1.5
ancho = 0.5
alto = 0.6
grosor = 0.05

# Crear la malla y el objeto base
mesh = bpy.data.meshes.new('MallaJardinera')
obj = bpy.data.objects.new('Jardinera', mesh)

bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bm = bmesh.new()

# Crear el cubo exterior
bmesh.ops.create_cube(bm, size=1.0)

# Escalar a las dimensiones correctas
for v in bm.verts:
    v.co.x *= largo / 2
    v.co.y *= ancho / 2
    v.co.z *= alto / 2

# Posicionar sobre el suelo
bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, alto / 2))

# Obtener la cara superior y ahuecar
face_superior = max([f for f in bm.faces if f.normal.z > 0.9], key=lambda f: f.calc_center_median().z)

res = bmesh.ops.inset_individual(bm, faces=[face_superior], thickness=grosor)

if 'faces' in res and res['faces']:
    bmesh.ops.extrude_face_region(bm, geom=res['faces'])
    for v in bm.verts:
        if v.select:
            v.co.z -= (alto - grosor)

# Liberar bmesh
bm.to_mesh(mesh)
bm.free()
mesh.update()