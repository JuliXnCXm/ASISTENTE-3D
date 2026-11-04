import bpy

# Crear una escena vacía si no existe
if not bpy.data.scenes:
    bpy.ops.scene.new(name="Escalera")

# Definir las dimensiones
altura_piso = 2.8
altura_total = altura_piso * 14
ancho_peldaño = 0.5
espacio_peldaño = 0.3
altura_baranda = 0.9
ancho_baranda = 0.1
offset_baranda = 0.15

# Crear el piso inferior
bpy.ops.mesh.primitive_cube_add(size=altura_piso, location=(0, 0, 0))
piso_inferior = bpy.context.object
piso_inferior.name = "Piso Inferior"

# Crear el piso superior
bpy.ops.mesh.primitive_cube_add(size=altura_piso, location=(0, 0, altura_piso * 14))
piso_superior = bpy.context.object
piso_superior.name = "Piso Superior"

# Crear los peldaños
for i in range(14):
    bpy.ops.mesh.primitive_cube_add(size=ancho_peldaño, location=(i * (ancho_peldaño + espacio_peldaño), 0, i * altura_piso))
    peldaño = bpy.context.object
    peldaño.name = f"Peldaño {i}"

# Crear las barandas
for i in range(14):
    bpy.ops.mesh.primitive_cube_add(size=ancho_baranda, location=(i * (ancho_peldaño + espacio_peldaño) + offset_baranda, altura_baranda / 2, i * altura_piso))
    baranda_izquierda = bpy.context.object
    baranda_izquierda.name = f"Baranda Izquierda {i}"
    
    bpy.ops.mesh.primitive_cube_add(size=ancho_baranda, location=(i * (ancho_peldaño + espacio_peldaño) + ancho_peldaño - offset_baranda, altura_baranda / 2, i * altura_piso))
    baranda_derecha = bpy.context.object
    baranda_derecha.name = f"Baranda Derecha {i}"

# Ajustar la escala para que todo encaje correctamente
bpy.context.scene.unit_settings.scale_type = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1.0

# Ajustar la vista
bpy.ops.view3d.view_all()
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = piso_inferior
bpy.context.view_layer.objects.active.select_set(True)
bpy.ops.view3d.view_center_object()