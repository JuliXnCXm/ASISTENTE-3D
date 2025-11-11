import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho = 6.0 # Dimensión X
largo = 8.0 # Dimensión Y
altura_min = 3.0
altura_max = 4.5
espesor = 0.2

# Vértices de la cara inferior de la cubierta
verts = [
    (-ancho/2, -largo/2, altura_min), # V0
    (ancho/2, -largo/2, altura_min),  # V1
    (ancho/2, largo/2, altura_max),   # V2
    (-ancho/2, largo/2, altura_max),  # V3
]

# Caras (solo una cara en este caso)
faces = [(0, 1, 2, 3)]

# Crear malla y objeto
mesh_data = bpy.data.meshes.new("CubiertaInclinadaMesh")
mesh_data.from_pydata(verts, [], faces)
mesh_data.update()

cubierta_obj = bpy.data.objects.new("CubiertaInclinada", mesh_data)

# Añadir a la escena
bpy.context.collection.objects.link(cubierta_obj)

# Dar espesor con un modificador
solidify_mod = cubierta_obj.modifiers.new(name="SolidifyCubierta", type='SOLIDIFY')
solidify_mod.thickness = espesor