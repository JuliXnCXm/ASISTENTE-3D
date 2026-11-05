import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Parámetros
altura_total = 3.0
radio_total = 0.9
radio_poste = 0.1
num_peldaños = 16
espesor_peldaño = 0.05
rotacion_total_grados = 270

# Poste central
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste, 
    depth=altura_total, 
    location=(0, 0, altura_total / 2)
)
poste = bpy.context.active_object
poste.name = "Poste_Central"

# Peldaños
altura_paso = altura_total / num_peldaños
ancho_peldaño = radio_total - radio_poste
rotacion_total_rad = math.radians(rotacion_total_grados)
angulo_paso = rotacion_total_rad / (num_peldaños - 1)

peldaños = []
for i in range(num_peldaños):
    z_actual = i * altura_paso
    angulo_actual = i * angulo_paso

    # Crear un peldaño base (como un cubo)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(radio_poste + ancho_peldaño / 2, 0, z_actual + espesor_peldaño / 2))
    peldaño = bpy.context.active_object
    peldaño.name = f"Peldaño_{i+1}"
    peldaño.dimensions = (ancho_peldaño, 0.6, espesor_peldaño)
    peldaños.append(peldaño)
    
    # Crear un objeto vacío para pivotar
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    pivote = bpy.context.active_object
    
    # Emparentar peldaño al pivote
    peldaño.parent = pivote
    
    # Rotar el pivote
    pivote.rotation_euler[2] = angulo_actual

# Limpieza (opcional): des-emparentar y aplicar transformaciones
for peldaño in peldaños:
    matriz_mundial = peldaño.matrix_world.copy()
    peldaño.parent = None
    peldaño.matrix_world = matriz_mundial

bpy.ops.object.delete(use_global=False, confirm=False) # Borra los pivotes vacíos restantes