import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración de la escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros
largo = 1.5
ancho = 0.5
alto = 0.6
espesor_pared = 0.05

# --- Crear el volumen exterior
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto / 2), scale=(largo, ancho, alto))
exterior = bpy.context.active_object
exterior.name = "JardineraExterior"

# --- Crear el volumen interior para el hueco
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto / 2), scale=(largo - 2*espesor_pared, ancho - 2*espesor_pared, alto))
interior = bpy.context.active_object
interior.name = "HuecoJardinera"

# --- Aplicar la operación booleana
mod_bool = exterior.modifiers.new(name='Boolean', type='BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = interior
bpy.context.view_layer.objects.active = exterior
bpy.ops.object.modifier_apply(modifier=mod_bool.name)
bpy.data.objects.remove(interior, do_unlink=True)

# --- Crear la tierra
alto_tierra = alto - 0.10 # 10cm del borde
largo_tierra = largo - 2*espesor_pared
ancho_tierra = ancho - 2*espesor_pared
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto_tierra / 2), scale=(largo_tierra, ancho_tierra, alto_tierra))
tierra = bpy.context.active_object
tierra.name = "TierraJardinera"