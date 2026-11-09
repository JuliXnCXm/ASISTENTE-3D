import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la torre ---
num_pisos = 6
diametro_torre = 16.0
altura_piso = 3.0
espesor_muro = 0.25

# --- Creación de la torre ---
altura_total = num_pisos * altura_piso
altura_actual = 0

for i in range(num_pisos):
    # Crear el muro del piso actual
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diametro_torre / 2,
        depth=espesor_muro,
        location=(0, 0, altura_actual + espesor_muro / 2),
        vertices=128
    )
    muro = bpy.context.active_object
    muro.name = f"Muro_Piso_{i+1}"

    # Crear la losa del piso actual
    altura_losa = altura_piso - espesor_muro
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diametro_torre / 2,
        depth=altura_losa,
        location=(0, 0, altura_actual + altura_losa / 2),
        vertices=128
    )
    losa = bpy.context.active_object
    losa.name = f"Losa_Piso_{i+1}"
    
    # Mover la losa para que quede encima del muro
    losa.location.z += espesor_muro / 2
    
    # Avanzar en la altura total
    altura_actual += altura_piso