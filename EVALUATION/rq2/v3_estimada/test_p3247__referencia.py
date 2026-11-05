import blender_arch as A
import bpy

A.limpiar_escena()

ancho_fachada = 10.0
alto_piso = 2.9
prof_celosia = 0.5

# --- BASE ARQUITECTÓNICA (DSL) ---

# Planta Baja
muro_pb = A.crear_muro("MuroPB", largo=ancho_fachada, alto=alto_piso, grosor=0.25, material="Estuco")
losa_p1 = A.crear_losa_rectangular("LosaP1", ancho=ancho_fachada, fondo=8.0, espesor=0.2, origen=(0, -4, alto_piso), material="Hormigon")
puerta_entrada = A.crear_puerta("PuertaEntrada", ancho=1.8, alto=2.4, prof_marco=0.1, origen=(-1.5, -0.125, 0), material_panel="Vidrio_Templado", material_marco="Marco_Negro")
A.abrir_vanos_batch_rectangulares(muro_pb, centros_world=[(-1.5, 0.125, 1.2)], ancho=1.8, alto=2.4)

# Planta Alta
muro_p1 = A.crear_muro("MuroP1", largo=ancho_fachada, alto=alto_piso, grosor=0.25, origen=(0, -prof_celosia, alto_piso), material="Muro_Pintura_Gris")
cubierta = A.crear_techo_plano("Cubierta", ancho=ancho_fachada, fondo=8.0 + prof_celosia, espesor=0.2, origen=(0, -4, alto_piso*2), material="Hormigon")
ventana_p1 = A.crear_ventana("VentanaP1", ancho=ancho_fachada - 1.0, alto=alto_piso - 0.4, prof_marco=0.1, origen=(0, -prof_celosia - 0.125, alto_piso + 0.2), material_marco="Marco_Negro", material_vidrio="Vidrio_Templado")
A.abrir_vanos_batch_rectangulares(muro_p1, centros_world=[(0, -prof_celosia, alto_piso + alto_piso/2)], ancho=ancho_fachada - 1.0, alto=alto_piso - 0.4)

# --- CELOSÍA DE MADERA (BPY) ---

# Crear un material de madera para las lamas
mat_madera = bpy.data.materials.new(name="MaderaLamas")
mat_madera.use_nodes = True
bsdf = mat_madera.node_tree.nodes.get('Principled BSDF')
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.3, 0.15, 0.05, 1)
    bsdf.inputs['Roughness'].default_value = 0.8

# Crear una lama prototipo
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho_fachada/2 + 0.1, 0.1, alto_piso + alto_piso/2))
lama_proto = bpy.context.active_object
lama_proto.name = "LamaMadera"
lama_proto.dimensions = (0.05, 0.1, alto_piso)
lama_proto.data.materials.append(mat_madera)

# Crear la celosía duplicando la lama
espaciado = 0.15
num_lamas = int(ancho_fachada / espaciado)
for i in range(1, num_lamas):
    nueva_lama = lama_proto.copy()
    nueva_lama.data = lama_proto.data.copy()
    nueva_lama.location.x += i * espaciado
    bpy.context.collection.objects.link(nueva_lama)

# --- ENTORNO ---
terreno = A.crear_terreno_plano("Suelo", ancho=20, fondo=15, origen=(0, -7.5, -0.05), material="Cesped")

# Iluminación y cámara
A.agregar_luz("LuzSol", tipo="SUN", ubicacion=(8, -6, 8), energia=3.5)
A.crear_camara("CamaraFachada", ubicacion=(0, -11, 4.5), rotacion=(75, 0, 0), activa=True)