import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros Generales ---
num_pisos = 4
alto_piso = 3.0
ancho_total = 15.0
grosor_muro = 0.2

alto_total = num_pisos * alto_piso

# --- Muro principal de la fachada ---
muro_fachada = A.crear_muro("MuroFachada", largo=ancho_total, alto=alto_total, grosor=grosor_muro, material="Muro_Pintura")

# --- Parámetros del Módulo Repetitivo ---
num_modulos_x = 3
ancho_modulo = ancho_total / num_modulos_x
ancho_balcon = 2.5
fondo_balcon = 1.2
espesor_losa = 0.2
ancho_puerta = 1.8
alto_puerta = 2.4

# --- Creación de Módulos en Bucle ---
for piso in range(num_pisos):
    z_base = piso * alto_piso
    
    # Losa de piso/techo que genera los balcones
    losa_piso = A.crear_losa_rectangular(f"Losa_Piso_{piso}", 
        ancho=ancho_total, 
        fondo=grosor_muro + fondo_balcon, 
        espesor=espesor_losa, 
        origen=(0, -fondo_balcon, z_base + alto_piso - espesor_losa), 
        material="Hormigon")

    for mod in range(num_modulos_x):
        x_base = mod * ancho_modulo
        
        # Origen del hueco de la puerta
        x_puerta = x_base + (ancho_modulo - ancho_puerta) / 2
        z_puerta = z_base + alto_puerta / 2
        
        # Abrir hueco para la puerta
        A.abrir_vanos_batch_rectangulares(muro_fachada, 
            centros_world=[(x_puerta + ancho_puerta/2, grosor_muro/2, z_puerta)], 
            ancho=ancho_puerta, 
            alto=alto_puerta)
            
        # Crear puerta acristalada
        A.crear_puerta(f"Puerta_{piso}_{mod}", 
            ancho=ancho_puerta, 
            alto=alto_puerta, 
            prof_marco=grosor_muro, 
            origen=(x_puerta, 0, z_base), 
            material_panel="Vidrio", 
            material_marco="Marco_Blanco")

        # Crear barandilla
        origen_baranda = (x_base + (ancho_modulo - ancho_balcon)/2, -fondo_balcon, z_base + alto_piso - espesor_losa)
        
        # Barandilla frontal
        A.crear_baranda_lineal(f"Baranda_Frente_{piso}_{mod}", largo=ancho_balcon, origen=origen_baranda, material="Metal")
        # Barandillas laterales
        b_lat_izq = A.crear_baranda_lineal(f"Baranda_Izq_{piso}_{mod}", largo=fondo_balcon, origen=origen_baranda, material="Metal")
        b_lat_izq.rotation_euler.z = 1.5708 # 90 deg
        b_lat_der = A.crear_baranda_lineal(f"Baranda_Der_{piso}_{mod}", largo=fondo_balcon, origen=(origen_baranda[0] + ancho_balcon, origen_baranda[1], origen_baranda[2]), material="Metal")
        b_lat_der.rotation_euler.z = 1.5708

# --- Cubierta Ajardinada ---
A.crear_piso("CapaVegetal", ancho=ancho_total, fondo=grosor_muro+fondo_balcon, espesor=0.2, origen=(0,-fondo_balcon, alto_total), material="Cesped")
peto = A.crear_muro("PetoCubierta", largo=ancho_total, alto=1.0, grosor=0.15, origen=(0,-fondo_balcon-0.15, alto_total), material="Hormigon")

# --- Configuración de Escena ---
A.agregar_luz("Sol", tipo="SUN", ubicacion=(-10, -15, 20), energia=3)
A.crear_camara("CamaraFachada", ubicacion=(7.5, 18, 8), rotacion=(75, 0, 180), activa=True)