import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
num_niveles = 3
altura_nivel = 1.5
retranqueo = 0.5
longitud = 10.0
espesor = 0.4

# Crear los niveles escalonados
for i in range(num_niveles):
    # Calcular la posición de cada nivel
    pos_y = i * retranqueo + espesor / 2
    pos_z = i * altura_nivel + altura_nivel / 2
    
    # Crear el bloque del nivel
    bpy.ops.mesh.primitive_cube_add(
        location=(0, pos_y, pos_z),
        scale=(longitud, espesor, altura_nivel)
    )
    muro_nivel = bpy.context.active_object
    muro_nivel.name = f"MuroContencion_Nivel_{i+1}"