import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y mobiliario estándar ---
hab = A.crear_habitacion('Oficina', ancho=4, fondo=3.5, alto=2.7, material_muro='Muro_Pintura', material_suelo='Parquet')
silla = A.crear_silla('Silla_Oficina', origen=(1.2, 1.2, 0), material='Tela_Gris')
silla.rotation_euler[2] = -0.8 # Girar hacia el escritorio

# --- Escritorio en L personalizado (bpy) ---
# Parte larga
bpy.ops.mesh.primitive_cube_add(location=(1, 2.25, 0.725))
parte_larga = bpy.context.active_object
parte_larga.name = 'Escritorio_Largo'
parte_larga.dimensions = (2.0, 0.6, 0.05)
bpy.ops.object.transform_apply(scale=True)

# Parte corta
bpy.ops.mesh.primitive_cube_add(location=(2.25, 1.0, 0.725))
parte_corta = bpy.context.active_object
parte_corta.name = 'Escritorio_Corto'
parte_corta.dimensions = (0.6, 1.4, 0.05)
bpy.ops.object.transform_apply(scale=True)

# Unir partes
parte_larga.select_set(True)
parte_corta.select_set(True)
bpy.context.view_layer.objects.active = parte_larga
bpy.ops.object.join()
A.asignar_material(parte_larga, 'Madera_Roble')

# Patas del escritorio
for x_pos in [0.05, 1.95]:
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, 2.5, 0.35))
    pata = bpy.context.active_object
    pata.dimensions = (0.05, 0.05, 0.7)
    pata.parent = parte_larga
    A.asignar_material(pata, 'Marco_Negro')
bpy.ops.mesh.primitive_cube_add(location=(2.5, 0.35, 0.35))
pata_esquina = bpy.context.active_object
pata_esquina.dimensions = (0.05, 0.05, 0.7)
pata_esquina.parent = parte_larga
A.asignar_material(pata_esquina, 'Marco_Negro')

# --- Estantería modular (bpy) ---
def crear_modulo(tam, loc, mat):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    cubo = bpy.context.active_object
    cubo.dimensions = (tam, tam, tam)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.inset(thickness=0.02, use_boundary=False)
    # Seleccionar caras internas para borrarlas
    bpy.ops.object.mode_set(mode='OBJECT')
    cubo.data.polygons[1].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
    A.asignar_material(cubo, mat)
    return cubo

crear_modulo(0.8, (0.4, 0.15, 2.0), 'Madera_Roble')
crear_modulo(0.5, (1.1, 0.15, 2.25), 'MDF_Blanco')
crear_modulo(0.5, (1.1, 0.15, 1.75), 'MDF_Blanco')
crear_modulo(0.6, (1.8, 0.15, 2.1), 'Madera_Roble')
crear_modulo(0.4, (2.4, 0.15, 1.9), 'MDF_Blanco')
crear_modulo(0.4, (2.4, 0.15, 2.3), 'MDF_Blanco')

# --- Iluminación y cámara ---
A.agregar_luz('Luz_Oficina', tipo='AREA', ubicacion=(2, 1.75, 2.5), energia=600)
luz_area = bpy.data.objects['Luz_Oficina']
luz_area.data.size = 2.0
A.crear_camara('Camara_Oficina', ubicacion=(5, 5, 2.5), rotacion=(70, 0, 135))