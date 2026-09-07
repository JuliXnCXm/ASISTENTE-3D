import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Terreno ---
terreno_ancho = 30
terreno_largo = 25
terreno_espesor = 0.1

bpy.ops.mesh.primitive_plane_add(size=terreno_ancho, enter_editmode=False, align='WORLD', location=(0, 0, terreno_espesor/2), scale=(1, 1, 1))
terreno = bpy.context.object
terreno.name = "Terreno"
terreno.scale = (terreno_ancho/2, terreno_largo/2, 1)

# Césped
bpy.ops.object.particle_generate(count=1000, step=0.5)
bpy.context.object.particle_settings.material = bpy.data.materials.new(name="GrassMaterial")
bpy.data.materials["GrassMaterial"].use_nodes = True
principled_bsdf = bpy.data.materials["GrassMaterial"].node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.1, 0.4, 0.1, 1)
principled_bsdf.inputs["Roughness"].default_value = 0.8
bpy.ops.object.particle_edit(edit_mode='EDIT')
bpy.ops.particle.randomize_scale(factor=0.2)
bpy.ops.object.particle_edit(edit_mode='OBJECT')

# --- Casa ---
ancho_casa = 10
largo_casa = 8
altura_casa = 5

# Crear la base de la casa
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura_casa/2), scale=(ancho_casa/2, largo_casa/2, altura_casa/2))
casa_base = bpy.context.object
casa_base.name = "Casa_Base"

# Segundo piso
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura_casa + 2.5), scale=(ancho_casa/2, largo_casa/2, altura_casa/2))
casa_piso2 = bpy.context.object
casa_piso2.name = "Casa_Piso2"

# --- Tejado ---
altura_tejado = 3
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura_casa + altura_tejado/2), scale=(ancho_casa/2, largo_casa/2, 1))
tejado = bpy.context.object
tejado.name = "Tejado"

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=1)
bpy.ops.object.mode_set(mode='OBJECT')

# Mover vértices para crear el tejado a dos aguas
tejado.data.vertices[0].co = (ancho_casa/2, 0, altura_casa + altura_tejado)
tejado.data.vertices[1].co = (-ancho_casa/2, 0, altura_casa + altura_tejado)
tejado.data.vertices[2].co = (0, largo_casa/2, altura_casa + altura_tejado)
tejado.data.vertices[3].co = (0, -largo_casa/2, altura_casa + altura_tejado)

# --- Árbol ---
altura_arbol = 8
radio_tronco = 0.3
radio_copa = 1.5

# Tronco
bpy.ops.mesh.primitive_cylinder_add(radius=radio_tronco, depth=altura_arbol/2, enter_editmode=False, align='WORLD', location=(5, 2, altura_arbol/2), scale=(1, 1, 1))
tronco = bpy.context.object
tronco.name = "Tronco"

# Copa
bpy.ops.mesh.primitive_uv_sphere_add(radius=radio_copa, enter_editmode=False, align='WORLD', location=(5, 2, altura_arbol), scale=(1, 1, 1))
copa = bpy.context.object
copa.name = "Copa"

# --- Materiales ---
material_casa = bpy.data.materials.new(name="MaterialCasa")
material_casa.use_nodes = True
principled_bsdf = material_casa.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.8, 0.7, 0.6, 1)
casa_base.data.materials.append(material_casa)
casa_piso2.data.materials.append(material_casa)

material_tejado = bpy.data.materials.new(name="MaterialTejado")
material_tejado.use_nodes = True
principled_bsdf = material_tejado.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.6, 0.3, 0.1, 1)
tejado.data.materials.append(material_tejado)

# --- Guardar ---
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])