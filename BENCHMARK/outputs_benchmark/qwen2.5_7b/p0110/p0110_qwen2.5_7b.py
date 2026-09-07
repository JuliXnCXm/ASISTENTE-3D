import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del peldaño
peldaño_ancho = 1.0
peldaño_huella = 0.3
peldaño_contrahuella = 0.18

# Definir la altura total de la escalera
altura_total = 15 * (peldaño_huella + peldaño_contrahuella)

# Crear los peldaños
for i in range(15):
    # Posición del peldaño actual
    x_pos = -7.5 + i * (peldaño_ancho + 0.3)
    
    # Crear el peldaño como un rectángulo
    bpy.ops.mesh.primitive_plane_add(size=peldaño_ancho, location=(x_pos, 0, 0))
    
    # Rotar el peldaño para que apunte hacia arriba
    obj = bpy.context.object
    obj.rotation_euler[2] = -1.5708
    
    # Mover el peldaño hacia arriba
    obj.location.z += i * (peldaño_huella + peldaño_contrahuella)
    
    # Ajustar la escala en z para darle altura
    obj.scale[2] = 0.18

# Guardar el archivo .blend si existe BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene[BLEND_OUT])