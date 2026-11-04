import blender_arch as A
import bpy
import math

A.limpiar_escena()

# 1. Base de la plaza
plaza = A.crear_terreno_plano('PlazaBase', ancho=20, fondo=20, espesor=0.2, origen=(-10, -10, -0.2), material='Porcelanato')

# 2. Fuente central con bpy
# Nivel inferior
base_fuente = A.crear_columna('FuenteBase', seccion='circ', diametro=6, alto=0.4, origen=(0, 0, 0), material='Hormigon')
bpy.ops.mesh.primitive_cylinder_add(radius=2.8, depth=0.3, location=(0, 0, 0.15))
agua_nivel1 = bpy.context.active_object
A.asignar_material(agua_nivel1, nombre='AguaFuente', base_color=(0.3, 0.6, 0.8, 0.7))

# Nivel superior
medio_fuente = A.crear_columna('FuenteMedio', seccion='circ', diametro=3, alto=0.8, origen=(0, 0, 0), material='Hormigon')
bpy.ops.mesh.primitive_cylinder_add(radius=1.3, depth=0.3, location=(0, 0, 0.55))
agua_nivel2 = bpy.context.active_object
A.asignar_material(agua_nivel2, nombre='AguaFuente', base_color=(0.3, 0.6, 0.8, 0.7))

# Chorro de agua central con modificador
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(0, 0, 1.5))
chorro = bpy.context.active_object
chorro.name = 'ChorroAgua'
chorro.scale.z = 2.5

# Aplicar textura procedural para simular movimiento de agua
if not 'AguaMovimiento' in bpy.data.textures:
    tex = bpy.data.textures.new('AguaMovimiento', type='CLOUDS')
    tex.noise_scale = 0.5

disp_mod = chorro.modifiers.new(name='DisplaceAgua', type='DISPLACE')
disp_mod.texture = bpy.data.textures['AguaMovimiento']
disp_mod.strength = 0.1
A.asignar_material(chorro, nombre='AguaFuente', base_color=(0.5, 0.8, 1.0, 0.6))

# 3. Bancos de hormigón a medida
perfil_banco = [(-1.5, 0), (1.5, 0), (1.5, 0.1), (0.3, 0.1), (0.3, 0.5), (-1.2, 0.5), (-1.5, 0.2), (-1.5, 0)]
for i in range(4):
    angulo = math.radians(i * 90 + 45)
    origen_x = math.cos(angulo) * 5
    origen_y = math.sin(angulo) * 5
    banco = A.extruir_perfil(f'Banco_{i}', puntos_2d=perfil_banco, altura=0.6, material='Hormigon')
    banco.location = (origen_x, origen_y, 0)
    banco.rotation_euler[2] = angulo + math.radians(90)

# 4. Pérgola de madera con bpy
# Columnas de la pérgola
for i in range(4):
    x = -6 + (i % 2) * 12
    y = -6 + (i // 2) * 12
    A.crear_columna(f'PostePergola_{i}', seccion='rect', ancho=0.25, fondo=0.25, alto=3.0, origen=(x, y, 0), material='Madera_Roble')

# Vigas principales
bpy.ops.mesh.primitive_cube_add(location=(-6, 0, 3.125), scale=(0.25, 6, 0.125))
bpy.context.active_object.name = 'VigaPrincipal_1'
bpy.ops.mesh.primitive_cube_add(location=(6, 0, 3.125), scale=(0.25, 6, 0.125))
bpy.context.active_object.name = 'VigaPrincipal_2'

# Vigas secundarias (patrón personalizado)
for i in range(15):
    x_pos = -7 + i * 1.0
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0, 3.375), scale=(0.075, 7, 0.125))
    viga = bpy.context.active_object
    viga.name = f'VigaSecundaria_{i}'

A.crear_camara(nombre='CamaraPlaza', ubicacion=(-12, -12, 8), rotacion=(65, 0, -45))