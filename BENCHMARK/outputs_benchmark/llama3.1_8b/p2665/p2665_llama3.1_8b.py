import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones y proporciones de los peldaños
huella = 0.28
contrahuella = 0.18
ancho_tramo = 1.0
alto_peldaño = 0.2

# Crea la geometría del tramo recto de escalera
for i in range(12):
    # Crea el peldaño actual
    bpy.ops.mesh.primitive_cube_add(size=alto_peldaño, location=(i * ancho_tramo + (ancho_tramo / 2), 0, -1))
    bpy.context.active_object.name = f"Peldaño {i+1}"
    
    # Crea la huella del peldaño actual
    bpy.ops.mesh.primitive_cube_add(size=huella, location=(i * ancho_tramo + (ancho_tramo / 2), 0, -1.01))
    bpy.context.active_object.name = f"Huella {i+1}"
    
    # Crea la contrahuella del peldaño actual
    bpy.ops.mesh.primitive_cube_add(size=contrahuella, location=(i * ancho_tramo + (ancho_tramo / 2), 0, -1.02))
    bpy.context.active_object.name = f"Contrahuella {i+1}"

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])