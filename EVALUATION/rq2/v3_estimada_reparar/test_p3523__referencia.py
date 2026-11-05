import blender_arch as A
import bpy

A.limpiar_escena()

# --- Materiales ---
muro_mat = 'Hormigon'
marco_mat = 'Marco_Negro'
vidrio_mat = 'Vidrio_Templado'

# --- Planta Baja ---
fachada_pb = A.crear_muro("Fachada_PB", largo=10, alto=3.0, grosor=0.3, material=muro_mat)
A.abrir_vanos_batch_rectangulares(fachada_pb, centros_world=[(2.5, 0.15, 1.4)], ancho=1.2, alto=2.8)
puerta = A.crear_puerta("PuertaEntrada", ancho=1.2, alto=2.8, prof_marco=0.1, origen=(2.5, 0.15, 0), material_panel="Madera_Nogal", material_marco=marco_mat)

# --- Planta Alta ---
losa_p1 = A.crear_losa_rectangular("Losa_P1", ancho=10, fondo=7, espesor=0.3, origen=(0, -6, 3.0), material=muro_mat)
fachada_p1 = A.crear_muro("Fachada_P1", largo=10, alto=3.0, grosor=0.3, origen=(0, -1, 3.0), material=muro_mat)
A.abrir_vanos_batch_rectangulares(fachada_p1, centros_world=[(0, -0.85, 4.5)], ancho=8, alto=2.6)
ventana_p1 = A.crear_ventana("Ventana_P1", ancho=8, alto=2.6, prof_marco=0.1, divisiones=(4,1), origen=(0, -0.85, 3.2), material_marco=marco_mat, material_vidrio=vidrio_mat)

# --- Cubierta ---
cubierta = A.crear_techo_plano("Cubierta", ancho=10, fondo=6.3, espesor=0.3, origen=(0, -6, 6.0), material=muro_mat)

# --- Detalles con BPY (Barandilla en cubierta) ---
def crear_barandilla_vidrio(nombre, origen, largo):
    # Postes
    for i in range(int(largo / 1.5) + 1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(origen[0] + i * 1.5, origen[1], origen[2] + 0.5))
        poste = bpy.context.active_object
        poste.name = f"{nombre}_Poste_{i}"
        poste.scale = (0.05, 0.05, 1.0)
        A.asignar_material(poste, nombre="Metal", base_color=(0.1, 0.1, 0.1, 1))
    # Pasamanos
    bpy.ops.mesh.primitive_cube_add(size=1, location=(origen[0] + largo/2 - 0.75, origen[1], origen[2] + 1.025))
    pasamanos = bpy.context.active_object
    pasamanos.name = f"{nombre}_Pasamanos"
    pasamanos.scale = (largo - 1.5, 0.08, 0.05)
    A.asignar_material(pasamanos, nombre="Metal", base_color=(0.1, 0.1, 0.1, 1))
    # Vidrio
    bpy.ops.mesh.primitive_cube_add(size=1, location=(origen[0] + largo/2 - 0.75, origen[1], origen[2] + 0.5))
    vidrio = bpy.context.active_object
    vidrio.name = f"{nombre}_Vidrio"
    vidrio.scale = (largo - 1.55, 0.01, 0.9)
    A.asignar_material(vidrio, nombre=vidrio_mat)

crear_barandilla_vidrio("Barandilla_Cubierta", origen=(-4.25, -0.85, 6.15), largo=8)

# --- Iluminación y Cámara ---
A.agregar_luz("LuzSol", tipo="SUN", ubicacion=(5, -10, 8), energia=2.0)
A.crear_camara("CamaraFachada", ubicacion=(0, -18, 4), rotacion=(80, 0, 0))