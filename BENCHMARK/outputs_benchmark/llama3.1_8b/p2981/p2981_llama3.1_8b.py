import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea un nuevo objeto cilíndrico
cylinder = bpy.data.objects.new("Cilindro", bpy.data.meshes.new("Cilindro"))

# Establece las propiedades del objeto
cylinder.location = (0, 0, 0)
cylinder.scale = (1, 1, 1)

# Crea la geometría cilíndrica
verts = [
    (-0.15, -0.15, 0),
    (0.15, -0.15, 0),
    (0.15, 0.15, 0),
    (-0.15, 0.15, 0)
]
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
]

faces = [
    (0, 1, 2, 3)
]

# Crea el polígono
cylinder.data.from_pydata(verts, edges, faces)
cylinder.data.update()

# Aplica la transformación de escala para obtener el diámetro correcto
scale_matrix = mathutils.Matrix.Scale(0.15, 4)
cylinder.matrix_world = scale_matrix.to_4x4() @ mathutils.Matrix.Translation((0, 0, 0.9))

# Agrega el objeto a la escena
bpy.context.collection.objects.link(cylinder)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])