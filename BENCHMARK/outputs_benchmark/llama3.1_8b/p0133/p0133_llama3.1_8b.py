import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de los peldaños
ancho_peldaño = 1.0
huella_peldaño = 0.3
contrahuella_peldaño = 0.18

# Crea un objeto para la escalera
escalera = bpy.data.objects.new("Escalera", None)

# Agrega el objeto a la escena
bpy.context.collection.objects.link(escalera)

# Define las coordenadas de los peldaños
coord_x = -7.5  # Coordenada x del primer peldaño

for i in range(15):
    # Crea un nuevo objeto para cada peldaño
    peldaño = bpy.data.objects.new(f"Peldaño {i+1}", None)
    
    # Agrega el objeto a la escena
    bpy.context.collection.objects.link(peldaño)

    # Establece las coordenadas del peldaño
    peldaño.location = (coord_x, 0, i * contrahuella_peldaño)
    
    # Define los vértices del peldaño
    vertices = [
        mathutils.Vector((ancho_peldaño / 2, huella_peldaño / 2, 0)),
        mathutils.Vector((-ancho_peldaño / 2, huella_peldaño / 2, 0)),
        mathutils.Vector((-ancho_peldaño / 2, -huella_peldaño / 2, 0)),
        mathutils.Vector((ancho_peldaño / 2, -huella_peldaño / 2, 0))
    ]
    
    # Crea un nuevo mesh para el peldaño
    mesh = bpy.data.meshes.new(f"Mesh Peldaño {i+1}")
    
    # Define los polígonos del peldaño
    faces = [
        (0, 1, 2),
        (2, 3, 0)
    ]
    
    # Crea el objeto de geometría para el peldaño
    obj_data = bpy.data.objects.new(f"Mesh Peldaño {i+1}", mesh)
    
    # Agrega el objeto a la escena
    bpy.context.collection.objects.link(obj_data)
    
    # Define los vértices y polígonos del peldaño
    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)
    
    # Establece las coordenadas del peldaño en el objeto de geometría
    obj_data.location = (coord_x, 0, i * contrahuella_peldaño)

    # Agrega el peldaño a la escalera
    bpy.ops.object.select_all(action='DESELECT')
    peldaño.select_set(True)
    bpy.context.collection.objects.link(peldaño)
    
    # Mueve el peldaño al objeto de geometría
    obj_data.location = (coord_x, 0, i * contrahuella_peldaño)

    coord_x += ancho_peldaño

# Guarda la escena si se especificó un archivo de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])