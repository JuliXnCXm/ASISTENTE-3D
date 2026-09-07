import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de los peldaños
ancho_peldaño = 1.0
huella_peldaño = 0.3
contrahuella_peldaño = 0.18

# Crea el tramo de escalera recto con 15 peldaños
for i in range(15):
    # Crea un nuevo objeto para cada peldaño
    bpy.ops.mesh.primitive_cube_add(size=ancho_peldaño, location=(i * ancho_peldaño, 0, 0))
    
    # Obtiene el objeto actual (último creado)
    obj = bpy.context.active_object
    
    # Renombra el objeto para que sea más fácil de identificar
    obj.name = f"Peldaño {i+1}"
    
    # Aplica la transformación de escala para darle la altura correcta al peldaño
    obj.scale[2] = contrahuella_peldaño
    
    # Aplica la transformación de rotación para que el peldaño esté en su posición correcta
    obj.rotation_euler[1] = mathutils.Vector((0, 0, 0))
    
    # Mueve el peldaño a su posición correcta en la escalera
    obj.location[2] = i * ancho_peldaño
    
    # Crea un nuevo objeto para cada contrahuella
    bpy.ops.mesh.primitive_cube_add(size=ancho_peldaño, location=(i * ancho_peldaño, 0, contrahuella_peldaño))
    
    # Obtiene el objeto actual (último creado)
    obj = bpy.context.active_object
    
    # Renombra el objeto para que sea más fácil de identificar
    obj.name = f"Contrahuella {i+1}"
    
    # Aplica la transformación de escala para darle la altura correcta a la contrahuella
    obj.scale[2] = huella_peldaño
    
    # Aplica la transformación de rotación para que la contrahuella esté en su posición correcta
    obj.rotation_euler[1] = mathutils.Vector((0, 0, 0))
    
    # Mueve la contrahuella a su posición correcta en la escalera
    obj.location[2] = i * ancho_peldaño + (ancho_peldaño / 2)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend con ese nombre
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])