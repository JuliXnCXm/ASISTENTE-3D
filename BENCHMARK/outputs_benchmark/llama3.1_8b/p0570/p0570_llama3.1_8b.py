import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el objeto base (edificio)
base = bpy.data.objects.new('Base', bpy.data.meshes.new('Base'))

# Define la geometría del edificio
verts = [
    (-10, -7.5, 0),
    (10, -7.5, 0),
    (10, 7.5, 0),
    (-10, 7.5, 0)
]

faces = [
    (0, 1, 2, 3)  # Cuadrado base
]

edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
]

# Crea la geometría del edificio
base.data.from_pydata(verts, edges, faces)
base.update(calc_edges=True)

# Agrega el objeto base a la escena
bpy.context.collection.objects.link(base)

# Crea los objetos de las paredes laterales y trasera
for i in range(5):
    # Pared lateral izquierda
    wall = bpy.data.objects.new(f'Pared Lateral Izquierda {i+1}', bpy.data.meshes.new(f'Pared Lateral Izquierda {i+1}'))
    
    verts = [
        (-10, -7.5 + i * 3, 0),
        (10, -7.5 + i * 3, 0),
        (10, -7.5 + i * 3, 2),
        (-10, -7.5 + i * 3, 2)
    ]

    faces = [
        (0, 1, 2, 3)  # Cuadrado pared
    ]

    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0)
    ]

    wall.data.from_pydata(verts, edges, faces)
    wall.update(calc_edges=True)

    bpy.context.collection.objects.link(wall)

    # Pared lateral derecha
    wall = bpy.data.objects.new(f'Pared Lateral Derecha {i+1}', bpy.data.meshes.new(f'Pared Lateral Derecha {i+1}'))
    
    verts = [
        (10, -7.5 + i * 3, 0),
        (-10, -7.5 + i * 3, 0),
        (-10, -7.5 + i * 3, 2),
        (10, -7.5 + i * 3, 2)
    ]

    faces = [
        (0, 1, 2, 3)  # Cuadrado pared
    ]

    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0)
    ]

    wall.data.from_pydata(verts, edges, faces)
    wall.update(calc_edges=True)

    bpy.context.collection.objects.link(wall)

    # Pared trasera
    wall = bpy.data.objects.new(f'Pared Trasera {i+1}', bpy.data.meshes.new(f'Pared Trasera {i+1}'))
    
    verts = [
        (-10, -7.5 + i * 3, 2),
        (10, -7.5 + i * 3, 2),
        (10, 7.5, 2),
        (-10, 7.5, 2)
    ]

    faces = [
        (0, 1, 2, 3)  # Cuadrado pared
    ]

    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0)
    ]

    wall.data.from_pydata(verts, edges, faces)
    wall.update(calc_edges=True)

    bpy.context.collection.objects.link(wall)

# Crea la fachada de muro cortina
for i in range(5):
    # Pared delantera
    wall = bpy.data.objects.new(f'Pared Delantera {i+1}', bpy.data.meshes.new(f'Pared Delantera {i+1}'))
    
    verts = [
        (-10, -7.5 + i * 3, 0),
        (10, -7.5 + i * 3, 0),
        (10, -7.5 + i * 3, 2),
        (-10, -7.5 + i * 3, 2)
    ]

    faces = [
        (0, 1, 2, 3)  # Cuadrado pared
    ]

    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0)
    ]

    wall.data.from_pydata(verts, edges, faces)
    wall.update(calc_edges=True)

    bpy.context.collection.objects.link(wall)

# Simula la fachada de muro cortina con una retícula de ventanas
for i in range(5):
    for j in range(20):
        # Ventana
        window = bpy.data.objects.new(f'Ventana {i+1}x{j+1}', bpy.data.meshes.new(f'Ventana {i+1}x{j+1}'))
        
        verts = [
            (j * 0.5, -7.5 + i * 3, 0),
            (j * 0.5 + 0.2, -7.5 + i * 3, 0),
            (j * 0.5 + 0.2, -7.5 + i * 3, 1),
            (j * 0.5, -7.5 + i * 3, 1)
        ]

        faces = [
            (0, 1, 2, 3)  # Cuadrado ventana
        ]

        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0)
        ]

        window.data.from_pydata(verts, edges, faces)
        window.update(calc_edges=True)

        bpy.context.collection.objects.link(window)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])