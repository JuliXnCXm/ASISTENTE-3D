import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la oficina
oficina_ancho = 8
oficina_largo = 6
oficina_altura = 2.8

# Crea el espacio principal
bpy.ops.mesh.primitive_cube_add(size=oficina_altura, location=(0, 0, -oficina_altura/2))
espacio_principal = bpy.context.active_object
espacio_principal.name = "Espacio Principal"

# Define las dimensiones de los puestos de trabajo
puesto_ancho = oficina_ancho / 4
puesto_largo = oficina_largo

# Crea cuatro puestos de trabajo idénticos
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=oficina_altura, location=(-oficina_ancho/2 + (i+1)*puesto_ancho/2, 0, -oficina_altura/2))
    puesto = bpy.context.active_object
    puesto.name = f"Puesto {i+1}"
    
    # Agrega un escritorio a cada puesto de trabajo
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-puesto_ancho/2 + (i+1)*puesto_ancho/2, 0, -oficina_altura/2))
    escritorio = bpy.context.active_object
    escritorio.name = f"Escritorio {i+1}"
    
    # Agrega una silla ergonómica a cada puesto de trabajo
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-puesto_ancho/2 + (i+1)*puesto_ancho/2, 0, -oficina_altura/2))
    silla = bpy.context.active_object
    silla.name = f"Silla {i+1}"
    
    # Agrega una cajonera a cada puesto de trabajo
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-puesto_ancho/2 + (i+1)*puesto_ancho/2, 0, -oficina_altura/2))
    cajonera = bpy.context.active_object
    cajonera.name = f"Cajonera {i+1}"

# Define las dimensiones de la sala de reuniones
sala_reuniones_ancho = oficina_ancho / 4
sala_reuniones_largo = oficina_largo

# Crea la sala de reuniones en una esquina
bpy.ops.mesh.primitive_cube_add(size=oficina_altura, location=(-oficina_ancho/2 + sala_reuniones_ancho/2, -oficina_largo/2 + sala_reuniones_largo/2, -oficina_altura/2))
sala_reuniones = bpy.context.active_object
sala_reuniones.name = "Sala de Reuniones"

# Agrega un tabique de vidrio entre la oficina y la sala de reuniones
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-oficina_ancho/2 + sala_reuniones_ancho/2 - 0.1, -oficina_largo/2 + sala_reuniones_largo/2 - 0.1, -oficina_altura/2))
tabique = bpy.context.active_object
tabique.name = "Tabique de Vidrio"

# Agrega una mesa grande para 6 personas en la sala de reuniones
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-oficina_ancho/2 + sala_reuniones_ancho/2 - 0.1, -oficina_largo/2 + sala_reuniones_largo/2 - 0.1, -oficina_altura/2))
mesa = bpy.context.active_object
mesa.name = "Mesa de Reuniones"

# Agrega seis sillas en la mesa de reuniones
for i in range(6):
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-oficina_ancho/2 + sala_reuniones_ancho/2 - 0.1, -oficina_largo/2 + sala_reuniones_largo/2 - 0.1, -oficina_altura/2))
    silla = bpy.context.active_object
    silla.name = f"Silla de Reunión {i+1}"

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])