import bpy

# --- Escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
diametro_base = 0.30
espesor_base = 0.02
altura_mastil = 1.5
radio_mastil = 0.015
altura_pantalla = 0.40
diametro_pantalla = 0.35

# --- Base ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_base / 2,
    depth=espesor_base,
    location=(0, 0, espesor_base / 2)
)
base = bpy.context.active_object
base.name = "BaseLampara"

# --- Mástil ---
loc_mastil_z = espesor_base + altura_mastil / 2
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_mastil,
    depth=altura_mastil,
    location=(0, 0, loc_mastil_z)
)
mastil = bpy.context.active_object
mastil.name = "MastilLampara"

# --- Pantalla (cilindro) ---
loc_pantalla_z = espesor_base + altura_mastil - altura_pantalla / 2
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_pantalla / 2,
    depth=altura_pantalla,
    location=(0, 0, loc_pantalla_z)
)
pantalla = bpy.context.active_object
pantalla.name = "PantallaLampara"

# --- Bombilla ---
loc_bombilla_z = espesor_base + altura_mastil - altura_pantalla / 2
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.05,
    location=(0, 0, loc_bombilla_z)
)
bombilla = bpy.context.active_object
bombilla.name = "Bombilla"

# Material emisivo (sin sockets viejos de Principled)
mat = bpy.data.materials.new(name="Emisivo")
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new("ShaderNodeOutputMaterial")
emi = nt.nodes.new("ShaderNodeEmission")
emi.inputs["Color"].default_value = (1.0, 0.8, 0.5, 1.0)
emi.inputs["Strength"].default_value = 10.0
nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])

bombilla.data.materials.clear()
bombilla.data.materials.append(mat)
