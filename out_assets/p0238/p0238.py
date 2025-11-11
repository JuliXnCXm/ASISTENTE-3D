import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

num_peldanos = 8
altura_total = 1.44
ancho_escalera = 1.5
huella = 0.3

contrahuella = altura_total / num_peldanos

# Peldaños
for i in range(num_peldanos):
    x_pos = (i * huella) + huella / 2
    y_pos = ancho_escalera / 2
    z_pos = (i * contrahuella) + contrahuella / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_pos, y_pos, z_pos),
        scale=(huella, ancho_escalera, contrahuella)
    )
    bpy.context.active_object.name = f"Peldano_{i+1}"

# Base tipo cuña (sin addons, sin bmesh): prisma triangular extruido en Y
largo_base = num_peldanos * huella
alto_base = num_peldanos * contrahuella

# Vértices (y=0 y y=ancho)
v0 = (0.0,           0.0, 0.0)
v1 = (largo_base,    0.0, 0.0)
v2 = (largo_base,    0.0, alto_base)
v3 = (0.0,           ancho_escalera, 0.0)
v4 = (largo_base,    ancho_escalera, 0.0)
v5 = (largo_base,    ancho_escalera, alto_base)

verts = [v0, v1, v2, v3, v4, v5]
faces = [
    [0,1,4,3],   # cara inferior
    [1,2,5,4],   # cara vertical en x = largo
    [2,0,3,5],   # cara inclinada
    [0,2,1],     # tapa triangular y=0
    [3,4,5],     # tapa triangular y=ancho
]

mesh = bpy.data.meshes.new("BaseEscaleraMesh")
mesh.from_pydata(verts, [], faces)
mesh.update()
base = bpy.data.objects.new("BaseEscalera", mesh)
bpy.context.collection.objects.link(base)
