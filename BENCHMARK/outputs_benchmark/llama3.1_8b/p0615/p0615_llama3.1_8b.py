import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo de porcelanato
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
suelo = bpy.context.active_object
suelo.name = "Suelo"
suelo.scale = (8, 6, 0.1)

# Crea la zona de estar con un sofá y una estantería
bpy.ops.mesh.primitive_cube_add(size=2, location=(3, -2, 0))
sofa = bpy.context.active_object
sofa.name = "Sofa"
sofa.scale = (4, 1.5, 1)

bpy.ops.mesh.primitive_cube_add(size=1, location=(3, -2, 1.5))
estanteria = bpy.context.active_object
estanteria.name = "Estantería"
estanteria.scale = (2, 0.5, 1)

# Crea la zona de comedor con una mesa y cuatro sillas
bpy.ops.mesh.primitive_cube_add(size=1, location=(-3, -2, 0))
mesa = bpy.context.active_object
mesa.name = "Mesa"
mesa.scale = (2, 1, 0.5)

for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-3 + i * 0.75, -2, 0))
    silla = bpy.context.active_object
    silla.name = "Silla"
    silla.scale = (1, 0.25, 0.25)

# Crea la luz de área en el techo
bpy.ops.mesh.primitive_circle_add(radius=1, location=(0, 0, 2))
luz_area = bpy.context.active_object
luz_area.name = "Luz de Área"
luz_area.scale = (4, 4, 1)

# Aplica materiales a los objetos
bpy.data.materials.new(name="Material_Suelo")
mat_suelo = bpy.data.materials["Material_Suelo"]
mat_suelo.use_nodes = True

bpy.data.materials.new(name="Material_Sofa")
mat_sofa = bpy.data.materials["Material_Sofa"]
mat_sofa.use_nodes = True

bpy.data.materials.new(name="Material_Estantería")
mat_estanteria = bpy.data.materials["Material_Estantería"]
mat_estanteria.use_nodes = True

bpy.data.materials.new(name="Material_Mesa")
mat_mesa = bpy.data.materials["Material_Mesa"]
mat_mesa.use_nodes = True

bpy.data.materials.new(name="Material_Silla")
mat_silla = bpy.data.materials["Material_Silla"]
mat_silla.use_nodes = True

bpy.data.materials.new(name="Material_Luz_Area")
mat_luz_area = bpy.data.materials["Material_Luz_Area"]
mat_luz_area.use_nodes = True

# Aplica el material al suelo
suelo.data.materials.append(mat_suelo)

# Aplica el material al sofá
sofa.data.materials.append(mat_sofa)

# Aplica el material a la estantería
estanteria.data.materials.append(mat_estanteria)

# Aplica el material a la mesa
mesa.data.materials.append(mat_mesa)

# Aplica el material a las sillas
for obj in bpy.context.scene.objects:
    if obj.name.startswith("Silla"):
        obj.data.materials.append(mat_silla)

# Aplica el material a la luz de área
luz_area.data.materials.append(mat_luz_area)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])