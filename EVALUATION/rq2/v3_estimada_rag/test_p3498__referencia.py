import bpy
import blender_arch as A

# --- Setup ---
A.limpiar_escena()

# --- Parámetros del edificio ---
num_pisos = 5
modulos_por_piso = 4
alto_piso = 3.0
ancho_modulo = 4.0
prof_balcon = 1.5
grosor_muro = 0.3
grosor_losa = 0.25

ancho_total = modulos_por_piso * ancho_modulo
alto_total = num_pisos * alto_piso

# --- Muro de fachada y cubierta ---
muro_fachada = A.crear_muro("MuroEdificio", largo=ancho_total, alto=alto_total, grosor=grosor_muro, material="Estuco")

cubierta = A.crear_techo_plano("CubiertaEdificio", ancho=ancho_total, fondo=grosor_muro, espesor=0.3, origen=(0, -grosor_muro/2, alto_total), material="Hormigon")

# --- Crear módulos repetitivos (balcones y huecos) ---
centros_vanos = []

for piso in range(num_pisos):
    z_piso = piso * alto_piso + grosor_losa # Nivel del suelo del balcón
    
    for modulo in range(modulos_por_piso):
        x_modulo = modulo * ancho_modulo
        
        # 1. Crear la losa del balcón
        origen_losa = (x_modulo, -prof_balcon - grosor_muro/2, z_piso - grosor_losa)
        losa_balcon = A.crear_losa_rectangular(f"Losa_P{piso}M{modulo}", ancho=ancho_modulo, fondo=prof_balcon, espesor=grosor_losa, origen=origen_losa, material="Concreto_Piso")
        
        # 2. Definir el hueco para la puerta corredera
        ancho_puerta = ancho_modulo - 0.5
        alto_puerta = alto_piso - grosor_losa - 0.2
        x_centro_puerta = x_modulo + ancho_modulo/2
        z_centro_puerta = z_piso + alto_puerta/2
        centros_vanos.append((x_centro_puerta, -grosor_muro/2, z_centro_puerta))
        
        # 3. Crear carpintería (representación simplificada)
        A.crear_ventana(f"Puerta_P{piso}M{modulo}", ancho=ancho_puerta, alto=alto_puerta, prof_marco=grosor_muro, divisiones=(2,1), origen=(x_centro_puerta, -grosor_muro/2, z_centro_puerta), material_marco="Marco_Aluminio", material_vidrio="Vidrio_Templado")

        # 4. Crear barandilla de vidrio con bpy
        altura_barandilla = 1.05
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_modulo + ancho_modulo/2, -prof_balcon, z_piso + altura_barandilla/2))
        panel_vidrio = bpy.context.object
        panel_vidrio.name = f"Barandilla_P{piso}M{modulo}"
        panel_vidrio.scale = (ancho_modulo - 0.1, 0.02, altura_barandilla/2)
        A.asignar_material(panel_vidrio, nombre="Vidrio_Esmerilado")
        
# --- Abrir todos los vanos en el muro ---
A.abrir_vanos_batch_rectangulares(muro_fachada, centros_vanos, ancho=ancho_modulo - 0.5, alto=alto_piso - grosor_losa - 0.2)

# --- Iluminación y Cámara ---
A.agregar_luz("LuzSolar", tipo="SUN", ubicacion=(10, -20, 15), energia=2.0)
A.crear_camara("CamaraPrincipal", ubicacion=(ancho_total/2, -25, alto_total/2.5), rotacion=(80, 0, 0), activa=True)