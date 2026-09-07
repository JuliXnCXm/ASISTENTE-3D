import bpy
import blender_arch as A

A.limpiar_escena()

# Base de la plaza
plaza_ancho = 25.0
plaza_fondo = 15.0
terreno = A.crear_terreno_plano("BasePlaza", ancho=plaza_ancho, fondo=plaza_fondo, espesor=0.2, origen=(0, 0, -0.1))
A.asignar_material(terreno, "Asfalto")

# Pavimento de adoquines con bpy
def crear_adoquin(origen, tamano=(0.2, 0.1, 0.08)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=origen)
    adoquin = bpy.context.active_object
    adoquin.scale = (tamano[0], tamano[1], tamano[2])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    A.asignar_material(adoquin, "Concreto_Piso")
    return adoquin

tamano_adoquin_x, tamano_adoquin_y = 0.2, 0.1
num_x = int(plaza_ancho / tamano_adoquin_x)
num_y = int(plaza_fondo / tamano_adoquin_y)

adoquin_maestro = crear_adoquin(origen=(-plaza_ancho/2, -plaza_fondo/2, 0.04), tamano=(tamano_adoquin_x, tamano_adoquin_y, 0.08))
mod_array_x = adoquin_maestro.modifiers.new(name='ArrayX', type='ARRAY')
mod_array_x.count = num_x
mod_array_x.relative_offset_displace[0] = 1.0
mod_array_x.relative_offset_displace[1] = 0.0

mod_array_y = adoquin_maestro.modifiers.new(name='ArrayY', type='ARRAY')
mod_array_y.count = num_y
mod_array_y.relative_offset_displace[0] = 0.0
mod_array_y.relative_offset_displace[1] = 1.0

# Árboles y alcorques
for i, x_pos in enumerate([-5, 5]):
    # Alcorque (borde)
    bpy.ops.mesh.primitive_cube_add(size=1.2, location=(x_pos, 3, 0.05))
    borde_alcorque = bpy.context.active_object
    borde_alcorque.scale.z = 0.1
    A.asignar_material(borde_alcorque, "Hormigon")
    bpy.ops.object.modifier_add(type='WIREFRAME')
    borde_alcorque.modifiers["Wireframe"].thickness = 0.1

    # Tierra
    tierra = A.crear_piso(f"TierraAlcorque_{i}", 1.0, 1.0, 0.1, origen=(x_pos, 3, 0))
    A.asignar_material(tierra, "Terreno")

    # Árbol
    A.crear_arbol_simple(f"ArbolPlaza_{i}", radio_copa=2.5, altura_copa=4.0, altura_tronco=2.5, origen=(x_pos, 3, 0.1))

# Bancas de diseño simple (bpy)
def crear_banca(origen, rotacion_z=0):
    # Base de hormigón
    bpy.ops.mesh.primitive_cube_add(location=(origen[0], origen[1], origen[2] + 0.2))
    base = bpy.context.active_object
    base.name = f"Banca_Base_{origen[0]}"
    base.scale = (2.0, 0.4, 0.4)
    A.asignar_material(base, "Hormigon")

    # Asiento de madera
    bpy.ops.mesh.primitive_cube_add(location=(origen[0], origen[1], origen[2] + 0.425))
    asiento = bpy.context.active_object
    asiento.name = f"Banca_Asiento_{origen[0]}"
    asiento.scale = (2.0, 0.4, 0.05)
    A.asignar_material(asiento, "Madera_Roble")
    base.rotation_euler.z = rotacion_z
    asiento.rotation_euler.z = rotacion_z
    
crear_banca(origen=(-6, -4, 0), rotacion_z=0.2)
crear_banca(origen=(0, -5, 0), rotacion_z=0)
crear_banca(origen=(6, -4, 0), rotacion_z=-0.2)

# Farolas (bpy)
def crear_farola(origen):
    # Poste
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=6.0, location=(origen[0], origen[1], origen[2] + 3.0))
    poste = bpy.context.active_object
    poste.name = f"Farola_Poste_{origen[0]}"
    A.asignar_material(poste, "Acero")
    # Luminaria
    bpy.ops.mesh.primitive_cube_add(location=(origen[0], origen[1], origen[2] + 6.0))
    luz = bpy.context.active_object
    luz.name = f"Farola_Luz_{origen[0]}"
    luz.scale = (0.2, 0.2, 0.2)
    A.asignar_material(luz, "Muro_Pintura") # Simula el difusor
    A.agregar_luz(f"PuntoLuz_{origen[0]}", tipo="POINT", ubicacion=(origen[0], origen[1], origen[2] + 5.8), energia=1500)

crear_farola(origen=(-10, -6, 0))
crear_farola(origen=(-10, 6, 0))
crear_farola(origen=(10, -6, 0))
crear_farola(origen=(10, 6, 0))

# Iluminación y cámara
A.agregar_luz("LuzSol", tipo="SUN", ubicacion=(5, -10, 15), energia=5)

A.crear_camara("CamaraPlaza", ubicacion=(-12, -15, 8), rotacion=(65, 0, -45), activa=True)