import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

ancho_total = 6.0
alto_total = 4.0
ancho_panel = 2.0
alto_panel = 2.0
ancho_perfil = 0.05
profundo_perfil = 0.10
grosor_vidrio = 0.01

num_paneles_x = int(ancho_total / ancho_panel)
num_paneles_y = int(alto_total / alto_panel)

# Material aluminio (Principled OK)
mat_aluminio = bpy.data.materials.new("Aluminio")
mat_aluminio.use_nodes = True
bsdf = mat_aluminio.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.2

# Material vidrio con Glass BSDF
mat_vidrio = bpy.data.materials.new("Vidrio")
mat_vidrio.use_nodes = True
nt = mat_vidrio.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new('ShaderNodeOutputMaterial')
glass = nt.nodes.new('ShaderNodeBsdfGlass')
glass.inputs['IOR'].default_value = 1.52
glass.inputs['Roughness'].default_value = 0.05
nt.links.new(glass.outputs['BSDF'], out.inputs['Surface'])

# Montantes (verticales)
for i in range(num_paneles_x + 1):
    loc_x = i * ancho_panel
    bpy.ops.mesh.primitive_cube_add(
        location=(loc_x, 0, alto_total / 2),
        scale=(ancho_perfil / 2, profundo_perfil / 2, alto_total / 2)
    )
    obj = bpy.context.object
    obj.name = f"Montante_{i}"
    obj.data.materials.append(mat_aluminio)

# Travesaños (horizontales)
for i in range(num_paneles_y + 1):
    loc_z = i * alto_panel
    bpy.ops.mesh.primitive_cube_add(
        location=(ancho_total / 2, 0, loc_z),
        scale=(ancho_total / 2, profundo_perfil / 2, ancho_perfil / 2)
    )
    obj = bpy.context.object
    obj.name = f"Travesano_{i}"
    obj.data.materials.append(mat_aluminio)

# Paneles de vidrio
for i in range(num_paneles_x):
    for j in range(num_paneles_y):
        loc_x = i * ancho_panel + ancho_panel / 2
        loc_z = j * alto_panel + alto_panel / 2
        bpy.ops.mesh.primitive_cube_add(
            location=(loc_x, 0, loc_z),
            scale=((ancho_panel - ancho_perfil) / 2, grosor_vidrio / 2, (alto_panel - ancho_perfil) / 2)
        )
        obj = bpy.context.object
        obj.name = f"Vidrio_{i}_{j}"
        obj.data.materials.append(mat_vidrio)

bpy.ops.object.select_all(action='DESELECT')
