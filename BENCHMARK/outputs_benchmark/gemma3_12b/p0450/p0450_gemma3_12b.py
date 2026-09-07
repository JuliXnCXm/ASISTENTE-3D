import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la cama (en metros)
longitud_cama = 2.0
ancho_cama = 1.0
altura_cama = 0.4

# Dimensiones del colchón (ligeramente más pequeño que la cama)
longitud_colchon = 1.9
ancho_colchon = 0.9
grosor_colchon = 0.2

# Dimensiones de la estructura de madera (patas y marco)
grosor_madera = 0.05
altura_patas = 0.3

# Crear la estructura de la cama (marco y patas)
def crear_estructura_cama():
    # Patas
    bpy.ops.mesh.primitive_cube_add(size=grosor_madera, location=(0, 0, altura_patas / 2))
    pata_frontal_izquierda = bpy.context.object
    pata_frontal_izquierda.scale = (0.1, 0.1, altura_patas / grosor_madera)
    pata_frontal_izquierda.name = "PataFrontalIzquierda"

    bpy.ops.mesh.primitive_cube_add(size=grosor_madera, location=(longitud_cama - 0.1, 0, altura_patas / 2))
    pata_frontal_derecha = bpy.context.object
    pata_frontal_derecha.scale = (0.1, 0.1, altura_patas / grosor_madera)
    pata_frontal_derecha.name = "PataFrontalDerecha"

    bpy.ops.mesh.primitive_cube_add(size=grosor_madera, location=(0, ancho_cama - 0.1, altura_patas / 2))
    pata_trasera_izquierda = bpy.context.object
    pata_trasera_izquierda.scale = (0.1, 0.1, altura_patas / grosor_madera)
    pata_trasera_izquierda.name = "PataTraseraIzquierda"

    bpy.ops.mesh.primitive_cube_add(size=grosor_madera, location=(longitud_cama - 0.1, ancho_cama - 0.1, altura_patas / 2))
    pata_trasera_derecha = bpy.context.object
    pata_trasera_derecha.scale = (0.1, 0.1, altura_patas / grosor_madera)
    pata_trasera_derecha.name = "PataTraseraDerecha"

    # Marco
    bpy.ops.mesh.primitive_cube_add(size=grosor_madera, location=(longitud_cama / 2, ancho_cama / 2, altura_cama))
    marco = bpy.context.object
    marco.scale = (longitud_cama / 2 / grosor_madera, ancho_cama / 2 / grosor_madera, 1)
    marco.name = "MarcoCama"

    return marco

marco_cama = crear_estructura_cama()

# Crear el colchón
bpy.ops.mesh.primitive_cube_add(size=1, location=(longitud_cama / 2, ancho_cama / 2, altura_cama - grosor_colchon / 2))
colchon = bpy.context.object
colchon.scale = (longitud_colchon / 2, ancho_colchon / 2, grosor_colchon / 2)
colchon.name = "Colchon"

# Aplicar material blanco al colchón
material_colchon = bpy.data.materials.new(name="MaterialColchon")
material_colchon.use_nodes = True
principled_bsdf = material_colchon.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)  # Blanco
colchon.data.materials.append(material_colchon)

# Aplicar material de madera al marco
material_madera = bpy.data.materials.new(name="MaterialMadera")
material_madera.use_nodes = True
principled_bsdf_madera = material_madera.node_tree.nodes["Principled BSDF"]
principled_bsdf_madera.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1)  # Madera
principled_bsdf_madera.inputs["Roughness"].default_value = 0.5
marco_cama.data.materials.append(material_madera)

# Guardar la escena si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])