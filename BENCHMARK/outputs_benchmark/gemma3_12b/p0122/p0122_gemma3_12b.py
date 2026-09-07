import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Parámetros
altura_total = 3.0
diametro = 1.8
num_escalones = 16
altura_escalon = altura_total / num_escalones
radio = diametro / 2.0
grosor_escalon = 0.1
ancho_escalon = 0.2
altura_poste = altura_total
radio_poste = 0.1

# Crear el poste central
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2.0),
    rotation=(0, 0, 0)
)
poste = bpy.context.object
poste.name = "PosteCentral"

# Crear los escalones
for i in range(num_escalones):
    angulo = i * (2 * math.pi / num_escalones)
    x = radio * math.cos(angulo)
    y = radio * math.sin(angulo)
    z = i * altura_escalon

    bpy.ops.mesh.primitive_plane_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(x, y, z),
        rotation=(0, 0, angulo - math.pi / 2.0)
    )
    escalon = bpy.context.object
    escalon.name = f"Escalon_{i+1}"
    escalon.scale = (ancho_escalon, grosor_escalon, 1.0)

# Unir los escalones
bpy.ops.object.select_all(action='DESELECT')
for i in range(num_escalones):
    escalon = bpy.data.objects[f"Escalon_{i+1}"]
    bpy.context.view_layer.objects.active = escalon
    escalon.select_set(True)

bpy.ops.object.join()

# Renombrar el objeto combinado
escalera_combinada = bpy.context.object
escalera_combinada.name = "EscaleraCaracol"

# Guardar el archivo .blend
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])