import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de los peldaños
ancho_peldaño = 1.0
huella_peldaño = 0.3
contrahuella_peldaño = 0.18

# Crea una nueva colección para la escalera
bpy.ops.object.collection_all()
escalera_collection = bpy.data.collections.new("Escalera")
bpy.context.scene.collection.children.link(escalera_collection)

# Crea los peldaños
for i in range(15):
    # Crea un nuevo objeto de tipo cuadrado
    peldaño = bpy.data.objects.new(f"Peldaño {i}", bpy.data.meshes.new("Peldaño"))

    # Establece la posición del peldaño
    peldaño.location = mathutils.Vector((0, 0.3 * i, 0))

    # Crea el cuadrado que representa el peldaño
    verts = [
        (-ancho_peldaño / 2, -huella_peldaño / 2, 0),
        (ancho_peldaño / 2, -huella_peldaño / 2, 0),
        (ancho_peldaño / 2, contrahuella_peldaño / 2, 0),
        (-ancho_peldaño / 2, contrahuella_peldaño / 2, 0)
    ]
    faces = [
        (0, 1, 2, 3)
    ]

    # Crea el objeto de cuadrado
    peldaño.data.from_pydata(verts, [], faces)
    peldaño.update_tag()

    # Agrega el peldaño a la colección de la escalera
    escalera_collection.objects.link(peldaño)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])