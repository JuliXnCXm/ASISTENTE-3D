import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura_cuerpo = 0.9
radio = 0.1

# Crear cuerpo del bolardo
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio,
    depth=altura_cuerpo,
    location=(0, 0, altura_cuerpo / 2)
)

# Crear tapa semiesférica
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio,
    location=(0, 0, altura_cuerpo)
)
sphere = bpy.context.active_object

# Cortar la esfera a la mitad (creando una nueva malla)
verts = [v.co for v in sphere.data.vertices if v.co.z >= 0]
new_mesh = bpy.data.meshes.new(name='HemiSphereMesh')

# Crear la malla a partir de los vértices (esto es complejo, una forma más simple es escalar)
bpy.data.objects.remove(sphere, do_unlink=True)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio,
    location=(0, 0, altura_cuerpo)
)
hemi = bpy.context.active_object
hemi.scale[2] = 0.5
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
hemi.location.z = altura_cuerpo