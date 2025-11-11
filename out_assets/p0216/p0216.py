import bpy

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

ancho_base = 8.0  # eje X
largo_base = 5.0  # eje Y
altura_cumbrera = 2.0
espesor = 0.2

# Construir prisma extruyendo un perfil hexagonal (sin bmesh)
# Perfil en plano XZ (6 puntos)
cs = [
    (-ancho_base/2, 0.0),                 # 0 alero izq exterior
    ( 0.0,           altura_cumbrera),     # 1 cumbrera exterior
    ( ancho_base/2,  0.0),                 # 2 alero der exterior
    ( ancho_base/2, -espesor),             # 3 alero der interior
    ( 0.0,           altura_cumbrera-espesor), # 4 cumbrera interior
    (-ancho_base/2, -espesor),             # 5 alero izq interior
]

y0 = -largo_base/2
y1 =  largo_base/2

verts = []
for y in (y0, y1):
    for (x, z) in cs:
        verts.append((x, y, z))

# Caras laterales (quads entre perfiles)
faces = []
N = len(cs)
for i in range(N):
    j = (i + 1) % N
    a = i
    b = j
    c = j + N
    d = i + N
    faces.append([a, b, c, d])

# Tapa frontal y trasera (hexágonos)
faces.append([0, 1, 2, 3, 4, 5])       # frente (y = y0)
faces.append([0+N, 5+N, 4+N, 3+N, 2+N, 1+N])  # atrás (y = y1), invertido

mesh = bpy.data.meshes.new("CubiertaDosAguas")
mesh.from_pydata(verts, [], faces)
mesh.update()

obj = bpy.data.objects.new("CubiertaDosAguas", mesh)
scene.collection.objects.link(obj)
obj.location = (0, 0, 0)
