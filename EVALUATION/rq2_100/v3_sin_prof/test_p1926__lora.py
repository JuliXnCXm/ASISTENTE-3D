import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y mobiliario base ---
habitacion = A.crear_habitacion('Oficina', ancho=3.0, fondo=2.5, alto=2.8, material_muro='Muro_Pintura_Gris', material_suelo='Parquet')
mesa_esquina = A.crear_mesa('Escritorio', ancho=1.4, fondo=0.7, alto=0.75, origen=(0.8, 0.8, 0), material_tablero='Madera_Roble')
silla = A.crear_silla('Silla_Oficina', origen=(1.5, 1.2, 0), material='Cuero')

# --- Librería paramétrica generada por código ---
def crear_estante_parametrico(nombre, largo, alto, prof, origen, material):
    bpy.ops.mesh.primitive_cube_add(location=origen)
    estante = bpy.context.active_object
    estante.name = nombre
    estante.dimensions = (largo, prof, alto)
    A.asignar_material(estante, nombre=material)
    return estante

ancho_total_libreria = 1.8
num_estantes = 5
grosor_estante = 0.05
separacion = 0.1

for i in range(num_estantes):
    pos_x = (i * (ancho_total_libreria / num_estantes)) + grosor_estante/2
    pos_y = 0.1
    pos_z = grosor_estante/2
    
    # Crear estante
    largo_estante = ancho_total_libreria / num_estantes
    estante = crear_estante_parametrico(f'Estante_{i+1}', largo=largo_estante, alto=2.2, prof=grosor_estante, origen=(pos_x, pos_y, pos_z), material='Madera_Roble')
    
    # Rotar estantes para que queden encajados
    estante.rotation_euler[2] = i * (3.14159 / num_estantes)

# --- Iluminación y cámara ---
A.agregar_luz('Luz_Techo', tipo='AREA', ubicacion=(1.5, 1.25, 2.7), energia=200)
A.crear_camara('Camara_Oficina', ubicacion=(-1.5, -1.5, 2.5), rotacion=(70, 0, 0))