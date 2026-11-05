import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros ---
ancho_edificio = 15.0
num_plantas = 4
ancho_modulo = 3.0
profundidad_modulo = 2.5
alto_piso = 3.0
grosor_muro = 0.25
grosor_losa = 0.2
ancho_baranda = 0.15
alto_baranda = 0.9

# --- Materiales ---
mat_muro = "Muro_Pintura_Gris"
mat_losa = "Hormigon"
mat_vidrio = "Vidrio_Templado"
mat_acero = "Acero_Inox"

# --- Crear edificio base ---
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Apartamentos",
    pisos=num_plantas,
    ancho=ancho_edificio,
    fondo=profundidad_modulo,
    alto_piso=alto_piso,
    grosor_muro=grosor_muro,
    con_techo_plano=True,
    material_muro=mat_muro,
    material_losa=mat_losa
)

# --- Crear balcones y barandillas ---
def crear_balcon(x_pos):
    # Balcon
    bpy.ops.mesh.primitive_cube_add(location=(x_pos + ancho_modulo/2, profundidad_modulo/2, alto_piso))
    balcon = bpy.context.active_object
    balcon.name = f"Balcon_{x_pos}"
    balcon.dimensions = (ancho_modulo, profundidad_modulo, 0.2)
    A.asignar_material(balcon, nombre=mat_muro, base_color=(0.8, 0.8, 0.8, 1))

    # Barandilla
    bpy.ops.mesh.primitive_cube_add(location=(x_pos + ancho_modulo/2, profundidad_modulo/2, alto_piso + 0.2 + ancho_baranda/2))
    barandilla = bpy.context.active_object
    barandilla.name = f"Barandilla_{x_pos}"
    barandilla.dimensions = (ancho_modulo, ancho_baranda, alto_baranda)
    A.asignar_material(barandilla, nombre=mat_acero)

    # Puerta
    bpy.ops.mesh.primitive_cube_add(location=(x_pos + ancho_modulo/2, profundidad_modulo/2, alto_piso + 0.2 + 0.5))
    puerta = bpy.context.active_object
    puerta.name = f"Puerta_{x_pos}"
    puerta.dimensions = (1.0, 0.9, 1.0)
    A.asignar_material(puerta, nombre=mat_acero)

    return balcon, barandilla, puerta

# Crear balcones y barandillas en cada módulo
for i in range(3):
    x_pos = i * ancho_modulo
    crear_balcon(x_pos)

# --- Crear azotea ajardinada ---
# Losa superior
losa_azotea = A.crear_losa_rectangular("Losa_Azotea", ancho=ancho_edificio, fondo=profundidad_modulo, espesor=0.2, origen=(0, 0, num_plantas*alto_piso), material=mat_losa)

# Vegetación
for z in range(num_plantas+1):
    for x in range(3):
        x_pos = x * ancho_modulo
        y_pos = profundidad_modulo / 2
        A.crear_planta(f"Planta_{x}_{z}", radio=0.5, altura=1.0, origen=(x_pos, y_pos, z*alto_piso + 0.2 + 0.5))