import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura_poste = 8.0
radio_poste = 0.1
largo_brazo = 1.5
radio_brazo = 0.08

# Crear poste vertical
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste, 
    depth=altura_poste, 
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "PosteFarola"

# Crear brazo horizontal
loc_brazo_y = largo_brazo / 2
loc_brazo_z = altura_poste - radio_brazo
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_brazo, 
    depth=largo_brazo, 
    location=(0, loc_brazo_y, loc_brazo_z)
)
brazo = bpy.context.active_object
brazo.name = "BrazoFarola"
brazo.rotation_euler[0] = 1.5708 # 90 grados en radianes

# Crear cabeza de la luminaria
bpy.ops.mesh.primitive_cube_add(
    size=0.4, 
    location=(0, largo_brazo, altura_poste - 0.3)
)
cabeza = bpy.context.active_object
cabeza.name = "CabezaLuminaria"

# Crear fuente de luz
loc_luz = (0, largo_brazo, altura_poste - 0.6)
luz_data = bpy.data.lights.new(name="LuzFarola", type='POINT')
luz_data.energy = 250 # Watts
luz_objeto = bpy.data.objects.new(name="LuzFarolaObjeto", object_data=luz_data)
bpy.context.collection.objects.link(luz_objeto)
luz_objeto.location = loc_luz