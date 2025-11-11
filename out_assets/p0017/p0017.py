import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros de la escalera
num_peldanios = 16
altura_total = 3.0
radio_escalera = 1.0
radio_poste = 0.1

ancho_peldanio = radio_escalera - radio_poste
espesor_peldanio = 0.05
altura_peldanio = altura_total / num_peldanios
angulo_total = 360  # Una vuelta completa
angulo_paso = math.radians(angulo_total / num_peldanios)

# Crear poste central
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste, 
    depth=altura_total, 
    location=(0, 0, altura_total / 2))
poste = bpy.context.active_object
poste.name = "PosteCentral"

# Crear peldaños
for i in range(num_peldanios):
    angulo = i * angulo_paso
    
    # Posición del peldaño
    x_loc = (radio_poste + ancho_peldanio / 2) * math.cos(angulo)
    y_loc = (radio_poste + ancho_peldanio / 2) * math.sin(angulo)
    z_loc = (i + 0.5) * altura_peldanio
    
    # Crear el peldaño como un cubo
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_loc, y_loc, z_loc),
        rotation=(0, 0, angulo)
    )
    peldanio = bpy.context.active_object
    peldanio.name = f"Peldanio_{i+1}"
    peldanio.scale = (ancho_peldanio, 0.4, espesor_peldanio)