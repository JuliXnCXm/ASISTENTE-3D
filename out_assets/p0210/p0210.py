import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
num_peldanos = 12
ancho_escalera = 1.0
altura_total = 2.16

# Calcular dimensiones del peldaño
contrahuella = altura_total / num_peldanos # Rise
huella = 0.30 # Tread

# Crear peldaños en un bucle
for i in range(num_peldanos):
    # Posición del peldaño actual
    x_pos = 0
    y_pos = i * huella + huella / 2
    z_pos = i * contrahuella + contrahuella / 2

    # Crear el peldaño como un cubo
    bpy.ops.mesh.primitive_cube_add(
        location=(x_pos, y_pos, z_pos)
    )
    peldano = bpy.context.object
    peldano.scale = (ancho_escalera / 2, huella / 2, contrahuella / 2)
    bpy.ops.object.transform_apply(scale=True)
    peldano.name = f"Peldano_{i+1}"

# Crear zancas laterales (stringers)
long_zanca_diag = ((num_peldanos * huella)**2 + altura_total**2)**0.5
ancho_zanca = 0.1
alto_zanca = 0.3
angulo = math.atan(altura_total / (num_peldanos * huella))

# Zanca 1
loc_z1 = (-ancho_escalera/2 - ancho_zanca/2, (num_peldanos * huella)/2, altura_total/2)
rot_z1 = (-angulo, 0, 0)
bpy.ops.mesh.primitive_cube_add(location=loc_z1)
zanca1 = bpy.context.object
zanca1.rotation_euler = rot_z1
zanca1.scale = (ancho_zanca/2, long_zanca_diag/2, alto_zanca/2)
bpy.ops.object.transform_apply(rotation=True, scale=True)

# Zanca 2
loc_z2 = (ancho_escalera/2 + ancho_zanca/2, (num_peldanos * huella)/2, altura_total/2)
bpy.ops.mesh.primitive_cube_add(location=loc_z2)
zanca2 = bpy.context.object
zanca2.rotation_euler = rot_z1
zanca2.scale = (ancho_zanca/2, long_zanca_diag/2, alto_zanca/2)
bpy.ops.object.transform_apply(rotation=True, scale=True)