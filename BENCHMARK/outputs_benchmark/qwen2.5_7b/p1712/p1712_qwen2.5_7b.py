import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del edificio
ancho = 15.0
altura_piso = 3.0
num_pisos = 3
espacio_ventana = 2.0

# Crear el piso inferior
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, 0, 0))
piso_inferior = bpy.context.object
piso_inferior.name = "Piso_Inferior"

# Crear los pisos superiores
for i in range(1, num_pisos):
    piso_superior = piso_inferior.copy()
    piso_superior.location.z += altura_piso * i
    bpy.context.collection.objects.link(piso_superior)

# Crear las ventanas
def crear_ventana(x, y, z):
    ventana = bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x + 0.5, y + 0.5, z))
    return ventana[0]

for piso in range(num_pisos):
    for x in range(int(ancho / espacio_ventana)):
        for y in range(4):  # Suponiendo que cada piso tiene 4 ventanas en ancho
            crear_ventana(x * espacio_ventana, y * 5.0, altura_piso * piso)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if "BLEND_OUT" in os.environ:
    blend_out = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)