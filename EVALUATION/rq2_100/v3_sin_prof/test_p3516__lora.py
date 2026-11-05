import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros ---
ancho_edificio = 15.0
num_plantas = 4
ancho_modulo = 3.0
fondo_modulo = 2.5
alto_piso = 3.0
grosor_muro = 0.3
grosor_losa = 0.2
ancho_baranda = 0.2
alto_baranda = 1.0

# --- Materiales ---
mat_muro = "Muro_Pintura_Gris"
mat_marco = "Marco_Negro"
mat_vidrio = "Vidrio_Templado"
mat_losa = "Hormigon"
mat_baranda = "Acero_Inox"

# --- Crear edificio ---
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Apartamentos",
    pisos=num_plantas,
    ancho=ancho_edificio,
    fondo=ancho_modulo * num_plantas,
    alto_piso=alto_piso,
    grosor_muro=grosor_muro,
    con_techo_plano=True,
    con_columnas=False,
    origen=(0, 0, 0),
    material_muro=mat_muro,
    material_losa=mat_losa
)

# --- Crear balcones y barandillas ---
for p in range(num_plantas):
    for i in range(3):
        x_pos = i * ancho_modulo + ancho_modulo / 2
        z_pos = p * alto_piso + alto_piso / 2
        
        # Balcon
        A.crear_losa_rectangular(f"Balcon_{p}_{i}", ancho=ancho_modulo, fondo=fondo_modulo, espesor=0.2, origen=(x_pos, 0, z_pos), material=mat_losa)
        
        # Barandilla
        bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0, z_pos + fondo_modulo/2))
        barandilla = bpy.context.active_object
        barandilla.name = f"Barandilla_{p}_{i}"
        barandilla.dimensions = (ancho_baranda, fondo_modulo, alto_baranda)
        A.asignar_material(barandilla, nombre=mat_baranda, base_color=(0.5, 0.5, 0.5, 1))

# --- Azotea ajardinada ---
A.crear_techo_plano("Azotea", ancho=ancho_edificio, fondo=ancho_modulo * num_plantas, espesor=0.2, origen=(0, 0, num_plantas * alto_piso), material=mat_losa)
A.crear_terreno_plano("Jardin_Azotea", ancho=ancho_edificio, fondo=ancho_modulo * num_plantas, espesor=0.2, origen=(0, 0, num_plantas * alto_piso + grosor_losa), material="Cesped")

# --- Iluminación y cámara ---
A.agregar_luz("Luz_Solar", tipo="SUN", ubicacion=(-10, -10, 20), energia=5)
A.crear_camara("Camara_Fachada", ubicacion=(ancho_edificio/2, -15, 8), rotacion=(70, 0, 0))