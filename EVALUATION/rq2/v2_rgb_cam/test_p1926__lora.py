import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESCRITORIO DE ESQUINA PERSONALIZADO ---
ancho_escri = 1.2
prof_escri = 0.7
alto_escri = 0.75
grosor_tablero = 0.04

# Tablero
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_escri - grosor_tablero / 2))
tablero = bpy.context.active_object
tablero.name = "Tablero_Escritorio"
tablero.dimensions = (ancho_escri, prof_escri, grosor_tablero)
A.asignar_material(tablero, nombre="Madera_Roble", base_color=(0.8, 0.6, 0.4, 1))

# Patas
pos_pata_x = ancho_escri / 2 - grosor_tablero * 2
pos_pata_y = prof_escri / 2 - grosor_tablero * 2
posiciones_patas = [
    (pos_pata_x, pos_pata_y, alto_escri / 2),
    (-pos_pata_x, pos_pata_y, alto_escri / 2),
    (pos_pata_x, -pos_pata_y, alto_escri / 2),
    (-pos_pata_x, -pos_pata_y, alto_escri / 2)
]
for i, pos in enumerate(posiciones_patas):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    pata = bpy.context.active_object
    pata.name = f"Pata_Escritorio_{i+1}"
    pata.dimensions = (grosor_tablero, grosor_tablero, alto_escri)
    A.asignar_material(pata, nombre="Metal_Negro")

# Unir partes
A.unir_objetos([tablero, pata for pata in bpy.data.objects if pata.name.startswith("Pata_Escritorio_")], nombre="Escritorio_Esquinero")

# --- SILLA ERGONÓMICA ---
silla = A.crear_silla(
    nombre="Silla_Oficina",
    origen=(0, -0.6, 0),
    material="Cuero"
)

# --- LIBRERÍA PARAMÉTRICA CON BLENDER_ARCH ---
ancho_lib = 1.8
alto_lib = 2.2
prof_lib = 0.3
num_estantes = 5
grosor_estante = 0.04

# Crear estantes en un bucle
espaciado = (ancho_lib - num_estantes * grosor_estante) / (num_estantes - 1)
for i in range(num_estantes):
    x_pos = -ancho_lib/2 + i * espaciado
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, 0, alto_lib/2))
    estante = bpy.context.active_object
    estante.name = f"Estante_Libreria_{i+1}"
    estante.dimensions = (grosor_estante, prof_lib, alto_lib)
    A.asignar_material(estante, nombre="Madera_Roble")

# Unir estantes
libreria = A.unir_objetos([estante for estante in bpy.data.objects if estante.name.startswith("Estante_Libreria_")], nombre="Libreria_Esquinera")

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz(nombre="Luz_Oficina", tipo="AREA", ubicacion=(-1, 1, 3), energia=200)
A.crear_camara(nombre="Camara_Oficina", ubicacion=(1, -2, 2), rotacion=(70, 0, 0))