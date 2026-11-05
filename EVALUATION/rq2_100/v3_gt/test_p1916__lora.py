import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y mobiliario base ---
muro_1 = A.crear_muro('Muro_Fondo', largo=5, alto=2.8, origen=(0,0,0), material='Muro_Pintura_Gris')
muro_2 = A.crear_muro('Muro_Lateral', largo=4, alto=2.8, origen=(0,0,0), rotacion_z=-90, material='Muro_Pintura_Gris')

escritorio = A.crear_mesa(
    nombre='Escritorio',
    ancho=1.4,
    fondo=0.7,
    alto=0.75,
    origen=(1.3, 0.15, 0),
    material_tablero='Madera'
)

estanteria = A.crear_estanteria(
    nombre='Estanteria_Libros',
    ancho=1.2,
    alto=2.2,
    fondo=0.3,
    num_estantes=5,
    origen=(-0.6, 0.1, 0),
    material='MDF_Blanco'
)

silla = A.crear_silla(
    nombre='Silla_Oficina',
    origen=(1.3, 0.7, 0),
    material='Cuero'
)

# --- Muebles adicionales y decoración ---
# Libros generados proceduralmente
for i in range(5):
    libro = bpy.data.objects.new(f'Libro_{i}', None)
    libro.location = (-0.6 + 0.3 * i, 0.1, 0.1 + 0.15 * i)
    A.asignar_material(libro, nombre='Tapa_Negra', base_color=(0.1, 0.1, 0.1, 1))

# Iluminación y cámara
A.agregar_luz('Luz_Principal', tipo='AREA', ubicacion=(2.5, 2, 2.5), energia=500)
A.crear_camara('Camara_Oficina', ubicacion=(2, -3, 2), rotacion=(70, 0, 0))