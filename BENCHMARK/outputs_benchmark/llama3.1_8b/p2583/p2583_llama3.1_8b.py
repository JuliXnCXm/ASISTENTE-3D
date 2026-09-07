import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la habitación y los objetos
habitacion = {
    'ancho': 4.0,
    'largo': 3.5,
    'altura_pared': 2.5,
}

cama = {
    'ancho': 1.0,
    'alto': 2.0,
    'profundidad': 0.2
}

mesita_noche = {
    'ancho': 0.4,
    'alto': 0.4,
    'profundidad': 0.5
}

# Crea la habitación
bpy.ops.mesh.primitive_cube_add(size=habitacion['largo'], location=(0, -habitacion['altura_pared']/2, 0))
bpy.context.active_object.name = "Pared Izquierda"
bpy.ops.transform.resize(value=(habitacion['ancho'], habitacion['altura_pared'], habitacion['altura_pared']))

bpy.ops.mesh.primitive_cube_add(size=habitacion['ancho'], location=(-habitacion['largo']/2, -habitacion['altura_pared']/2, 0))
bpy.context.active_object.name = "Pared Fondo"
bpy.ops.transform.resize(value=(habitacion['ancho'], habitacion['altura_pared'], habitacion['altura_pared']))

bpy.ops.mesh.primitive_cube_add(size=habitacion['largo'], location=(-habitacion['ancho']/2, -habitacion['altura_pared']/2, 0))
bpy.context.active_object.name = "Pared Derecha"
bpy.ops.transform.resize(value=(habitacion['largo'], habitacion['altura_pared'], habitacion['altura_pared']))

bpy.ops.mesh.primitive_cube_add(size=habitacion['ancho'], location=(-habitacion['ancho']/2, -habitacion['largo']/2, 0))
bpy.context.active_object.name = "Piso"
bpy.ops.transform.resize(value=(habitacion['ancho'], habitacion['altura_pared'], habitacion['altura_pared']))

# Crea la cama
bpy.ops.mesh.primitive_cube_add(size=cama['alto'], location=(-(habitacion['ancho']-cama['ancho'])/2, -habitacion['altura_pared']/2+cama['profundidad'], 0))
bpy.context.active_object.name = "Cama"
bpy.ops.transform.resize(value=(cama['ancho'], cama['alto'], cama['profundidad']))

# Crea la mesita de noche
bpy.ops.mesh.primitive_cube_add(size=mesita_noche['alto'], location=(-(habitacion['ancho']-cama['ancho'])/2+mesita_noche['ancho'], -habitacion['altura_pared']/2+cama['profundidad']+mesita_noche['profundidad'], 0))
bpy.context.active_object.name = "Mesita Noche"
bpy.ops.transform.resize(value=(mesita_noche['ancho'], mesita_noche['alto'], mesita_noche['profundidad']))

# Guarda el archivo .blend si se especificó la ruta
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])