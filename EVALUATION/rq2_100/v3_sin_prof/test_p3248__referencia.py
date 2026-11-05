import blender_arch as A
import bpy

A.limpiar_escena()

num_pisos = 4
ancho_fachada = 15.0
alto_piso = 3.0
prof_balcon = 1.5
ancho_balcon = 4.0
separacion_balcon = 0.5

def crear_baranda_vidrio(nombre, origen, ancho):
    # Paneles de vidrio
    num_paneles = 3
    ancho_panel = (ancho - 0.1) / num_paneles
    for i in range(num_paneles):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(origen[0] - ancho/2 + ancho_panel/2 + i*ancho_panel, origen[1], origen[2] + 0.5))
        panel = bpy.context.active_object
        panel.name = f"{nombre}_Panel_{i}"
        panel.dimensions = (ancho_panel - 0.02, 0.02, 1.0)
        A.asignar_material(panel, "Vidrio_Templado")
    
    # Postes de acero
    for i in range(num_paneles + 1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(origen[0] - ancho/2 + i*ancho_panel, origen[1], origen[2] + 0.5))
        poste = bpy.context.active_object
        poste.name = f"{nombre}_Poste_{i}"
        poste.dimensions = (0.05, 0.05, 1.05)
        A.asignar_material(poste, "Acero_Inox")

# --- ESTRUCTURA PRINCIPAL (DSL) ---
muro_principal = A.crear_muro("MuroFachada", largo=ancho_fachada, alto=alto_piso * num_pisos, grosor=0.25, material="Estuco")

# Crear pisos y balcones
for i in range(num_pisos):
    z = (i + 1) * alto_piso
    A.crear_losa_rectangular(f"Losa_P{i}", ancho=ancho_fachada, fondo=12, espesor=0.2, origen=(0, -6, z), material="Hormigon")
    
    # Balcones (2 por planta)
    x1 = -(ancho_balcon + separacion_balcon) / 2
    x2 = (ancho_balcon + separacion_balcon) / 2
    
    A.crear_losa_rectangular(f"Balcon_P{i}_1", ancho=ancho_balcon, fondo=prof_balcon, espesor=0.2, origen=(x1, -prof_balcon/2, z-0.2), material="Hormigon")
    A.crear_losa_rectangular(f"Balcon_P{i}_2", ancho=ancho_balcon, fondo=prof_balcon, espesor=0.2, origen=(x2, -prof_balcon/2, z-0.2), material="Hormigon")
    
    # Puertas vidrieras
    A.abrir_vanos_batch_rectangulares(muro_principal, centros_world=[(x1, 0.125, z - alto_piso/2 + 0.1), (x2, 0.125, z - alto_piso/2 + 0.1)], ancho=2.8, alto=2.6)
    A.crear_ventana(f"PuertaVidriera_P{i}_1", ancho=2.8, alto=2.6, prof_marco=0.1, origen=(x1, -0.125, z - alto_piso + 0.1), material_marco="Marco_Aluminio", material_vidrio="Vidrio")
    A.crear_ventana(f"PuertaVidriera_P{i}_2", ancho=2.8, alto=2.6, prof_marco=0.1, origen=(x2, -0.125, z - alto_piso + 0.1), material_marco="Marco_Aluminio", material_vidrio="Vidrio")

    # --- BARANDILLAS (bpy) ---
    crear_baranda_vidrio(f"Baranda_P{i}_1_Frente", origen=(x1, -prof_balcon, z-0.1), ancho=ancho_balcon)
    crear_baranda_vidrio(f"Baranda_P{i}_2_Frente", origen=(x2, -prof_balcon, z-0.1), ancho=ancho_balcon)

# --- CUBIERTA AJARDINADA (bpy) ---
z_cubierta = num_pisos * alto_piso
A.crear_muro("PetoCubierta", largo=ancho_fachada, alto=0.8, grosor=0.2, origen=(0, 0.1, z_cubierta), material="Estuco")
A.crear_losa_rectangular("SueloJardin", ancho=ancho_fachada-0.4, fondo=11.6, espesor=0.4, origen=(0, -5.8, z_cubierta), material="Terreno")

# Jardineras perimetrales
for i in range(10):
    A.crear_arbol_simple(f"Arbusto_{i}", radio_copa=0.5, altura_copa=0.6, altura_tronco=0.1, origen=(-ancho_fachada/2 + 1 + i*1.5, -11.0, z_cubierta+0.4))

# --- ENTORNO ---
terreno = A.crear_terreno_plano("Suelo", ancho=25, fondo=20, origen=(0, -10, -0.1), material="Asfalto")

# Iluminación y cámara
A.agregar_luz("LuzSol", tipo="SUN", ubicacion=(10, -15, 12), energia=4.0)
A.crear_camara("CamaraFachada", ubicacion=(0, -18, 8), rotacion=(75, 0, 0), activa=True)