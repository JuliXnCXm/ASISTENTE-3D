import bpy

# Crear una nueva escena
bpy.ops.scene.new(name="Oficina")

# Configurar el tamaño del edificio
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1.0

# Crear el suelo
bpy.ops.mesh.primitive_cube_add(size=20, enter_editmode=False, align='WORLD', location=(0, 0, 0))
bpy.context.object.name = "Suelo"
bpy.context.object.location.z += 0.5

# Crear las columnas
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=3, enter_editmode=False, align='WORLD', location=(i*5, 0, 0))
    bpy.context.object.name = f"Columna{i}"
    bpy.context.object.location.z += 0.5

# Crear las ventanas
for i in range(4):
    for j in range(4):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(i*5+2.5, j*3.75+1.875, 0))
        bpy.context.object.name = f"Ventana{i}{j}"

# Crear los pisos
for i in range(8):
    bpy.ops.mesh.primitive_cube_add(size=20, enter_editmode=False, align='WORLD', location=(0, 0, i*2.5))
    bpy.context.object.name = f"Piso{i}"
    bpy.context.object.location.z += 0.5

# Finalizar la escena
bpy.context.scene.name = "Edificio de Oficinas"