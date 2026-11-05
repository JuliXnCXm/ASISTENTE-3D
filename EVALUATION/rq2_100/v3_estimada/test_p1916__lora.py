import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y mobiliario base ---
muro_1 = A.crear_muro('Muro_Fondo', largo=5, alto=2.8, origen=(0, 0, 0), material='Muro_Pintura_Gris')
muro_2 = A.crear_muro('Muro_Lateral', largo=4, alto=2.8, origen=(0, 0, 0), rotacion_z=-90, material='Muro_Pintura_Gris')

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
    origen=(-1.1, 0.1, 0),
    material='MDF_Blanco'
)

silla = A.crear_silla(
    nombre='Silla_Oficina',
    origen=(1.3, 0.7, 0),
    material='Cuero'
)

# --- Muebles adicionales con primitivas ---
# Taburete bajo
taburete = bpy.data.objects.new('Taburete', None)
bpy.context.collection.objects.link(taburete)
taburete.location = (1.3, 1.5, 0)
A.asignar_material(taburete, nombre='Cuero', base_color=(0.8, 0.6, 0.4, 1))

# Escritorio con Blender
bpy.ops.mesh.primitive_cube_add(location=(1.3, 0.15, 0.375))
escritorio_tablero = bpy.context.active_object
escritorio_tablero.name = 'Escritorio_Tablero'
escritorio_tablero.scale = (1.4, 0.7, 0.05)
A.asignar_material(escritorio_tablero, nombre='Madera_Roble')

bpy.ops.mesh.primitive_cube_add(location=(1.3, 0.15, 0.75))
escritorio_pata1 = bpy.context.active_object
escritorio_pata1.name = 'Escritorio_Pata1'
escritorio_pata1.scale = (0.05, 0.7, 0.4)
A.asignar_material(escritorio_pata1, nombre='Acero_Inox')

bpy.ops.mesh.primitive_cube_add(location=(1.3 + 1.4/2, 0.15, 0.75))
escritorio_pata2 = bpy.context.active_object
escritorio_pata2.name = 'Escritorio_Pata2'
escritorio_pata2.scale = (0.05, 0.7, 0.4)
A.asignar_material(escritorio_pata2, nombre='Acero_Inox')