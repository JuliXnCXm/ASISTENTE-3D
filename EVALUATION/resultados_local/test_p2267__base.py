import bpy

# Crear una fuente central de varios niveles
def create_multi_level_fountain():
    bpy.ops.mesh.primitive_cube_add(size=5, location=(0, 0, 0))
    bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, 2))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 4))
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 6))

# Crear bancos de hormigón a medida
def create_concrete_benches(length=5, height=0.5):
    for i in range(3):  # Se crean tres bancos
        bpy.ops.mesh.primitive_cube_add(size=length, location=(i*length+length/2, 0, height))
        bpy.ops.mesh.primitive_cube_add(size=length, location=(i*length+length/2, length, height))
        bpy.ops.mesh.primitive_cube_add(size=length, location=(i*length+length/2, 2*length, height))

# Crear una pérgola de madera con un patrón de vigas personalizado
def create_wooden_pergola(length=10, height=3, pattern='zigzag'):
    if pattern == 'zigzag':
        for i in range(0, length, 2):
            bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i, 0, height))
            bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i+1, length, height))
    else:
        print("Patrón no soportado")

# Ejecutar las funciones
create_multi_level_fountain()
create_concrete_benches()
create_wooden_pergola()