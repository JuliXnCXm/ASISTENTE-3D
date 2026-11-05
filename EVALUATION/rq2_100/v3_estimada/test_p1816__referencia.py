import blender_arch as A
import bpy

A.limpiar_escena()

# 1. Estructura de la habitación
hab = A.crear_habitacion('Cocina', ancho=5, fondo=4.5, alto=2.8, grosor_muro=0.15, 
                           material_muro='Muro_Pintura_Gris', material_suelo='Porcelanato')

# 2. Muebles bajos con blender_arch
mueble_largo = A.crear_armario('Mueble_Bajo_Largo', ancho=3, alto=0.9, fondo=0.6, num_puertas=4, origen=(0.15, 0.15, 0), material_cuerpo='MDF_Blanco')
mueble_corto = A.crear_armario('Mueble_Bajo_Corto', ancho=2, alto=0.9, fondo=0.6, num_puertas=3, origen=(3.15, 0.15, 0), material_cuerpo='MDF_Blanco')
mueble_corto.rotation_euler[2] = 1.5708 # 90 grados

# 3. Encimeras personalizadas con bpy
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.65, 1.8, 0.925))
encimera_larga = bpy.context.active_object
encimera_larga.name = 'Encimera_Larga'
encimera_larga.dimensions = (3.3, 0.65, 0.05)
A.asignar_material(encimera_larga, 'Concreto_Piso', base_color=(0.2, 0.2, 0.2, 1))

bpy.ops.mesh.primitive_cube_add(size=1, location=(3.475, 1.15, 0.925))
encimera_corta = bpy.context.active_object
encimera_corta.name = 'Encimera_Corta'
encimera_corta.dimensions = (0.65, 2.0, 0.05)
A.asignar_material(encimera_corta, 'Concreto_Piso', base_color=(0.2, 0.2, 0.2, 1))

# 4. Fregadero integrado con operación booleana
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5, 1.8, 0.92))
corte_fregadero = bpy.context.active_object
corte_fregadero.name = 'Corte_Fregadero'
corte_fregadero.dimensions = (0.6, 0.45, 0.2)
corte_fregadero.display_type = 'WIRE'
bool_mod = encimera_larga.modifiers.new(name='BooleanFregadero', type='BOOLEAN')
bool_mod.object = corte_fregadero
bool_mod.operation = 'DIFFERENCE'
bpy.context.view_layer.objects.active = encimera_larga
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(corte_fregadero)

# 5. Isla central
isla = A.crear_armario('Isla_Base', ancho=1.8, alto=0.9, fondo=0.9, num_puertas=2, origen=(1.6, 3, 0), material_cuerpo='Madera_Roble')
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.6+0.9, 3+0.45, 0.925))
encimera_isla = bpy.context.active_object
encimera_isla.name = 'Encimera_Isla'
encimera_isla.dimensions = (2.0, 1.1, 0.05)
A.asignar_material(encimera_isla, 'Concreto_Piso', base_color=(0.2, 0.2, 0.2, 1))

# 6. Luces colgantes sobre la isla usando bpy
for i, offset_x in enumerate([-0.6, 0, 0.6]):
    # Cable
    bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.8, location=(1.6+0.9+offset_x, 3+0.45, 2.4))
    cable = bpy.context.active_object
    cable.name = f'Cable_Luz_{i+1}'
    A.asignar_material(cable, 'Marco_Negro')
    # Pantalla de la lámpara
    bpy.ops.mesh.primitive_cone_add(radius1=0.15, depth=0.2, location=(1.6+0.9+offset_x, 3+0.45, 2.0))
    pantalla = bpy.context.active_object
    pantalla.name = f'Pantalla_Luz_{i+1}'
    A.asignar_material(pantalla, 'Cobre')
    # Luz
    A.agregar_luz(f'Luz_Isla_{i+1}', tipo='POINT', ubicacion=(1.6+0.9+offset_x, 3+0.45, 1.9), energia=150, color=(1, 0.8, 0.6))