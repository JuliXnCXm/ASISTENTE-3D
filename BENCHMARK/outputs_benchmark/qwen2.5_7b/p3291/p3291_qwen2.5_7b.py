import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
edificio_altura = 10
edificio_ancho = 20
edificio_largo = 30
suelo_deck_madera_tamano = (5, 5)
jardinera_hormigon_tamano = (0.5, 0.5, 0.8)
pergola_acero_altura = 4
pergola_acero_ancho = 6

# Crear el edificio
bpy.ops.mesh.primitive_cube_add(size=1, location=(edificio_largo/2 - edificio_ancho/2, edificio_ancho/2 - edificio_largo/2, edificio_altura))
edificio_objeto = bpy.context.object
edificio_objeto.scale = (edificio_largo, edificio_ancho, edificio_altura)

# Crear el suelo de deck de madera
bpy.ops.mesh.primitive_plane_add(size=suelo_deck_madera_tamano[0] + 1, location=(0, 0, -0.2))
suelo_objeto = bpy.context.object
suelo_objeto.scale = (suelo_deck_madera_tamano[0], suelo_deck_madera_tamano[1], 0.05)
bpy.ops.transform.resize(value=(1, 1, edificio_altura - 0.2))

# Crear las jardineras perimetrales de hormigón
for x in [-edificio_ancho/2 + suelo_deck_madera_tamano[0]/2, edificio_ancho/2 - suelo_deck_madera_tamano[0]/2]:
    for z in [-edificio_largo/2 + suelo_deck_madera_tamano[1]/2, edificio_largo/2 - suelo_deck_madera_tamano[1]/2]:
        bpy.ops.mesh.primitive_cube_add(size=jardinera_hormigon_tamano[0], location=(x, 0, z))
        jardinera_objeto = bpy.context.object
        jardinera_objeto.scale = (jardinera_hormigon_tamano[0], jardinera_hormigon_tamano[1], jardinera_hormigon_tamano[2])
        jardinera_objeto.rotation_euler[2] = 1.57

# Crear la pérgola de acero
bpy.ops.mesh.primitive_cube_add(size=pergola_acero_ancho, location=(0, 0, edificio_altura - pergola_acero_altura/2))
pergola_objeto = bpy.context.object
pergola_objeto.scale = (pergola_acero_ancho, suelo_deck_madera_tamano[1], pergola_acero_altura)
bpy.ops.transform.resize(value=(1, 1, edificio_altura - 0.2))

# Ajustar la escena para que todo esté en el mismo plano
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.location[2] = 0

if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])