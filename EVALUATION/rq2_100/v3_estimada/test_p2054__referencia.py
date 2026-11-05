import blender_arch as A
import bpy

A.limpiar_escena()
bpy.context.scene.unit_settings.system = 'METRIC'

# 1. Base de la isla con blender_arch
isla_base = A.crear_armario('Isla_Base', ancho=2.2, alto=0.9, fondo=1.0, num_puertas=3, origen=(0, 0, 0), material_cuerpo='MDF_Blanco')

# 2. Encimera personalizada con bpy
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.1, 0.5, 0.925))
encimera = bpy.context.active_object
encimera.name = 'Encimera_Cuarzo'
encimera.dimensions = (2.3, 1.1, 0.05)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
A.asignar_material(encimera, nombre='Cuarzo_Blanco', base_color=(0.9, 0.9, 0.9, 1))

# 3. Fregadero (hueco) con modificador Boolean en bpy
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5, 0.5, 0.925))
hueco_fregadero = bpy.context.active_object
hueco_fregadero.name = 'Cutter_Fregadero'
hueco_fregadero.dimensions = (0.5, 0.45, 0.2)
hueco_fregadero.display_type = 'WIRE'

bool_mod = encimera.modifiers.new(name='Fregadero', type='BOOLEAN')
bool_mod.object = hueco_fregadero
bool_mod.operation = 'DIFFERENCE'

# 4. Grifo simple con bpy
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.25, location=(1.78, 0.5, 1.025))
grifo_base = bpy.context.active_object
grifo_base.name = 'Grifo_Base'
bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.2, location=(1.68, 0.5, 1.15))
grifo_canon = bpy.context.active_object
grifo_canon.name = 'Grifo_Cañon'
grifo_canon.rotation_euler[1] = 1.5708 # 90 grados en Y
A.asignar_material(grifo_base, nombre='Acero_Inox')
A.asignar_material(grifo_canon, nombre='Acero_Inox')

# 5. Lámparas colgantes con blender_arch y bpy
for i in range(3):
    x_pos = 0.6 + i * 0.6
    # Luz
    A.agregar_luz(f'Luz_Colgante_{i}', tipo='POINT', ubicacion=(x_pos, 0.5, 2.0), energia=150, color=(1.0, 0.8, 0.6))
    # Cable (bpy)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.005, depth=0.8, location=(x_pos, 0.5, 2.4))
    bpy.context.active_object.name = f'Cable_{i}'
    # Pantalla (bpy)
    bpy.ops.mesh.primitive_cone_add(radius1=0.15, depth=0.2, location=(x_pos, 0.5, 2.0))
    pantalla = bpy.context.active_object
    pantalla.name = f'Pantalla_{i}'
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    pantalla.modifiers['Solidify'].thickness = 0.005

A.crear_piso('Suelo_Cocina', 6, 6, origen=(-1.9,-2.5,0), material='Parquet')