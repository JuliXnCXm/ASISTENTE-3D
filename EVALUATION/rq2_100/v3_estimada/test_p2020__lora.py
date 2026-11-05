import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y MUEBLES ---
ancho_salon = 4.0
fondo_salon = 3.2
alto_salon = 2.8
grosor_muro = 0.15

hab = A.crear_habitacion(
    nombre="Salon",
    ancho=ancho_salon,
    fondo=fondo_salon,
    alto=alto_salon,
    grosor_muro=grosor_muro,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Mueble de TV bajo
mueble_tv = A.crear_armario(
    nombre="Mueble_TV",
    ancho=1.2,
    alto=0.4,
    fondo=0.3,
    num_puertas=1,
    origen=(0, -fondo_salon/2 + 0.15 + 0.15, 0),
    material_cuerpo="MDF_Blanco"
)

# --- PARED DE ACCENTO CON LISTONES ---
ancho_liston = 0.02
separacion_liston = 0.01
num_listones = int((ancho_salon - 2 * grosor_muro) / (ancho_liston + separacion_liston))

# Crear el primer listón como un cubo
liston_base = bpy.data.objects.new("Liston_Base", None)
liston_base.location = (ancho_salon/2, 0, 1.8)
bpy.context.collection.objects.link(liston_base)

# Aplicar modificador Array para crear la fila de listones
array_mod = liston_base.modifiers.new(name="ArrayListones", type='ARRAY')
array_mod.count = num_listones
array_mod.use_relative_offset = False
array_mod.use_object_offset = True
array_mod.offset_object = liston_base
array_mod.relative_offset_displace[0] = 0
array_mod.relative_offset_displace[1] = 0
array_mod.relative_offset_displace[2] = 0

# Darle espesor a los listones
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.context.object.data.polygons[0].select = True # Seleccionar cara frontal
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={'value':(0, 0, 0.02)})
bpy.ops.object.mode_set(mode='OBJECT')

# Crear el material para los listones
mat_liston = A.crear_material("Liston_Madera", base_color=(0.7, 0.5, 0.3, 1))
liston_base.data.materials.append(mat_liston)

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz("Luz_Salon", tipo="AREA", ubicacion=(-1, 1, 2.5), energia=200)
A.crear_camara("Camara_Salon", ubicacion=(1, -2, 1.5), rotacion=(70, 0, 0))