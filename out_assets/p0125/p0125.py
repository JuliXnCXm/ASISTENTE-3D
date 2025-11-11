import bpy

# --- Escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
ancho_total = 3.0
alto_total = 2.2
grosor_marco = 0.10
espesor_vidrio = 0.01

# --- Marco como diferencia de cubos ---
# Cubo exterior
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, alto_total/2),
    scale=(ancho_total/2, grosor_marco/2, alto_total/2)
)
marco = bpy.context.active_object
marco.name = "MarcoVentana"

# Cubo interior (para vaciar)
inner_x = (ancho_total - 2*grosor_marco)/2
inner_z = (alto_total - 2*grosor_marco)/2
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, alto_total/2),
    scale=(inner_x, grosor_marco, inner_z)  # Y más grande para cortar a través
)
corte = bpy.context.active_object
corte.name = "CorteMarco"

mod = marco.modifiers.new(name='Boolean', type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = corte

bpy.context.view_layer.objects.active = marco
marco.select_set(True)
bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.data.objects.remove(corte, do_unlink=True)

# --- Panel de vidrio ---
ancho_vidrio = ancho_total - 2 * grosor_marco
alto_vidrio = alto_total - 2 * grosor_marco
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, alto_total/2),
    scale=(ancho_vidrio/2, espesor_vidrio/2, alto_vidrio/2)
)
vidrio = bpy.context.active_object
vidrio.name = "PanelVidrio"

# Material de vidrio con Glass BSDF (sin Transmission en Principled)
mat_vid = bpy.data.materials.new("Vidrio")
mat_vid.use_nodes = True
nt = mat_vid.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new('ShaderNodeOutputMaterial')
glass = nt.nodes.new('ShaderNodeBsdfGlass')
glass.inputs['IOR'].default_value = 1.52
glass.inputs['Roughness'].default_value = 0.05
nt.links.new(glass.outputs['BSDF'], out.inputs['Surface'])

vidrio.data.materials.clear()
vidrio.data.materials.append(mat_vid)
