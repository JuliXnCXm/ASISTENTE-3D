import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros
num_peldaños = 16
altura_total = 3.0
radio_escalera = 1.0
radio_poste = 0.1
grosor_peldaño = 0.05

# Poste central
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_total,
    location=(0, 0, altura_total / 2)
)

# Peldaños
altura_peldaño = altura_total / num_peldaños
angulo_paso = (2 * math.pi) / num_peldaños

for i in range(num_peldaños):
    angulo = i * angulo_paso
    
    # Usamos un cubo como base para el peldaño
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, 0) # Se posiciona después
    )
    peldaño = bpy.context.active_object
    peldaño.scale = (radio_escalera - radio_poste, 0.4, grosor_peldaño)
    
    # Posición y rotación
    x_loc = (radio_poste + (radio_escalera - radio_poste) / 2) * math.cos(angulo)
    y_loc = (radio_poste + (radio_escalera - radio_poste) / 2) * math.sin(angulo)
    z_loc = (i * altura_peldaño) + grosor_peldaño/2
    
    peldaño.location = (x_loc, y_loc, z_loc)
    peldaño.rotation_euler[2] = angulo