import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y MUEBLES ---
ancho_salon = 4.0
fondo_salon = 3.0
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
    origen=(0, -fondo_salon/2 + 0.3/2 + 0.05, 0),
    material_cuerpo="MDF_Blanco"
)

# --- PARED DE ACCENTO CON LISTONES ---
ancho_liston = 0.02
fondo_liston = 0.04
num_listones = 20
separacion_listones = 0.02

# Muro base para los listones
muro_listones = A.crear_muro(
    nombre="Pared_Acento",
    largo=ancho_salon,
    alto=2.4,
    grosor=grosor_muro,
    origen=(-ancho_salon/2, 0, 0),
    material="Madera_Roble"
)

# Modificador Array para crear listones
mod_array = muro_listones.modifiers.new(name="Listones", type='ARRAY')
mod_array.count = num_listones
mod_array.use_relative_offset = False
mod_array.use_object_offset = True
mod_array.offset_object = bpy.data.objects["Mueble_TV"]
mod_array.relative_offset_displace[0] = 0
mod_array.relative_offset_displace[1] = 0
mod_array.relative_offset_displace[2] = 0
mod_array.constant_offset_displace[0] = separacion_listones
mod_array.constant_offset_displace[1] = 0
mod_array.constant_offset_displace[2] = 0

# Crear listones
for i in range(num_listones):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * separacion_listones - ancho_salon/2 + ancho_liston/2, 0, 1.2)
    )
    liston = bpy.context.active_object
    liston.name = f"Liston_{i+1}"
    liston.dimensions = (ancho_liston, fondo_liston, 0.05)
    A.asignar_material(liston, "Madera_Roble")

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz("Luz_Salon", tipo="AREA", ubicacion=(0, 0, 2.5), energia=600)
A.crear_camara("Camara_Salon", ubicacion=(0, -5, 1.5), rotacion=(80, 0, 0))