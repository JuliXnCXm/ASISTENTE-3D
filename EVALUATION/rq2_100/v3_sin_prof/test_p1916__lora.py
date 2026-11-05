import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y mobiliario base ---
muro_1 = A.crear_muro('Muro_Fondo', largo=5, alto=2.8, origen=(0,0,0), material='Muro_Pintura_Gris')
muro_2 = A.crear_muro('Muro_Lateral', largo=4, alto=2.8, origen=(0,0,0), rotacion_z=90, material='Muro_Pintura_Gris')

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

# --- Muebles adicionales generados proceduralmente ---
def crear_estante_vertical():
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    estante = bpy.context.active_object
    estante.name = 'Estante_Vertical'
    estante.dimensions = (0.1, 0.3, 0.05)
    bpy.ops.object.transform_apply(scale=True)
    return estante

def crear_estante_horizontal():
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    estante = bpy.context.active_object
    estante.name = 'Estante_Horizontal'
    estante.dimensions = (0.3, 0.05, 0.1)
    bpy.ops.object.transform_apply(scale=True)
    return estante

def crear_libro():
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    libro = bpy.context.active_object
    libro.name = 'Libro'
    libro.dimensions = (0.2, 0.02, 0.03)
    bpy.ops.object.transform_apply(scale=True)
    return libro

def crear_estanteria_libros(num_estantes):
    espaciado = 0.05
    for i in range(num_estantes):
        altura = i * (0.05 + 0.02) + 0.02
        if i == 0:
            altura = 0.02
        elif i == num_estantes-1:
            altura = 0.05 + 0.02
        
        # Estantes verticales
        for j in [-1, 1]:
            pos_x = j * (0.1/2 + 0.05)
            crear_estante_vertical().location = (pos_x, 0, altura)
        
        # Estantes horizontales
        for k in [-1, 1]:
            pos_y = k * (0.3/2 + 0.05)
            crear_estante_horizontal().location = (0, pos_y, altura)
    
    # Libros
    for j in [-1, 1]:
        pos_x = j * (0.1/2 + 0.05)
        for k in [-1, 1]:
            pos_y = k * (0.3/2 + 0.05)
            for l in range(10):
                crear_libro().location = (pos_x, pos_y, altura + 0.03 + l * 0.02)
                crear_libro().scale.z = 0.005
                crear_libro().rotation_euler[0] = 1.5708 # 90 grados

crear_estanteria_libros(5)

# --- Iluminación y cámara ---
A.agregar_luz('Luz_Principal', tipo='AREA', ubicacion=(2.5, 2, 2.5), energia=200)
A.crear_camara('Camara_Oficina', ubicacion=(2, -3, 1.5), rotacion=(75, 0, 45))